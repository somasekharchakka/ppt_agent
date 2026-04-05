"""
agent_ppt.py — Multi-server agentic loop using Mistral's native tool calling.
Passes template name & slide count into the system prompt so the LLM
always calls initialize_presentation with the right parameters.
"""
import asyncio
import os
import sys
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from contextlib import AsyncExitStack

# Hardcoded absolute paths to the MCP servers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_SCRIPTS = [
    os.path.join(BASE_DIR, "servers", "ppt_mcp_server.py"),
    os.path.join(BASE_DIR, "servers", "search_mcp_server.py"),
    os.path.join(BASE_DIR, "servers", "filesystem_mcp_server.py"),
    os.path.join(BASE_DIR, "servers", "image_mcp_server.py"),
]

OUTPUT_PATH = os.path.join(BASE_DIR, "output.pptx")


async def run_ppt_agent(
    user_request: str,
    template: str = "corporate_professional",
    slide_count: int = 5,
    callbacks=None,
):
    """
    Main agentic loop.
    Returns a dict with key 'output' containing the agent's final text.
    """
    print(f"[AGENT] Prompt : {user_request}")
    print(f"[AGENT] Theme  : {template}")
    print(f"[AGENT] Slides : {slide_count}")

    # ── Load API key ─────────────────────────────────────────────────────
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("MISTRAL_API_KEY="):
                    os.environ["MISTRAL_API_KEY"] = line.strip().split("=", 1)[1]

    if not os.getenv("MISTRAL_API_KEY"):
        msg = "MISTRAL_API_KEY is not set. Add it to .env"
        print(f"[WARNING] {msg}")
        return {"output": msg}

    # ── Connect to all MCP servers ───────────────────────────────────────
    print("[AGENT] Connecting to MCP servers …")
    async with AsyncExitStack() as stack:
        tool_map: dict = {}        # name → async callable
        tools_for_llm: list = []   # JSON-Schema tool defs for Mistral

        for script in SERVER_SCRIPTS:
            params = StdioServerParameters(command=sys.executable, args=[script])
            transport = await stack.enter_async_context(stdio_client(params))
            read, write = transport
            session = await stack.enter_async_context(ClientSession(read, write))
            await session.initialize()

            for tool in (await session.list_tools()).tools:
                # closure that captures tool_name + session correctly
                async def _exec(tool_name=tool.name, sess=session, **kwargs):
                    try:
                        res = await sess.call_tool(tool_name, arguments=kwargs)
                        return res.content[0].text if res.content else "OK"
                    except Exception as exc:
                        return f"Error calling {tool_name}: {exc}"

                tool_map[tool.name] = _exec
                tools_for_llm.append(
                    {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.inputSchema,
                        },
                    }
                )

        print(f"[AGENT] {len(tool_map)} tools loaded: {list(tool_map.keys())}")

        # ── Build LLM with tools ─────────────────────────────────────────
        llm = ChatMistralAI(
            model="mistral-large-latest",
            temperature=0.7,
            timeout=180,
        )
        llm_with_tools = llm.bind_tools(tools_for_llm)

        save_path = OUTPUT_PATH.replace("\\", "\\\\")

        messages = [
            SystemMessage(
                content=f"""You are a Presentation Agent.  Your ONLY job is to
create a PowerPoint file on disk.

WORKFLOW — follow these steps IN ORDER:
1. Call `search_wikipedia` one or two times to gather facts about the topic.
2. Call `initialize_presentation` with:
   - topic  = a short title for the presentation
   - template = "{template}"
   - slide_count = {slide_count}
3. Call `write_slide` exactly {slide_count} times.
   • Each slide must have a title and 3-5 bullet points.
   • For at least 2 of those slides, provide an `image_query`
     (a short phrase to fetch a relevant photo, e.g. "machine learning robot").
4. Call `save_ppt` with filename = "{save_path}"
5. Return a Final Answer confirming the file was saved.

RULES:
- You MUST call the tools.  Do NOT simulate or pretend.
- Do NOT skip save_ppt.  The task fails if the file does not exist.
- Keep bullet points concise (1-2 sentences each).
"""
            ),
            HumanMessage(content=user_request),
        ]

        # ── Agentic loop ─────────────────────────────────────────────────
        print("[AGENT] Starting agentic loop …")
        MAX_TURNS = 20
        final_output = ""

        for turn in range(1, MAX_TURNS + 1):
            print(f"\n[TURN {turn}]")
            ai_msg = await llm_with_tools.ainvoke(messages)
            messages.append(ai_msg)

            if not ai_msg.tool_calls:
                final_output = ai_msg.content
                print(f"[AGENT] Final answer received.")
                break

            for tc in ai_msg.tool_calls:
                t_name = tc["name"]
                t_args = tc["args"]
                t_id   = tc["id"]
                print(f"  → Tool: {t_name}  Args: {json.dumps(t_args, default=str)[:200]}")

                if t_name in tool_map:
                    obs = await tool_map[t_name](**t_args)
                    # Truncate very long observations for the context window
                    if len(obs) > 1500:
                        obs = obs[:1500] + " … [truncated]"
                    print(f"  ← Observation: {obs[:150]}")
                    messages.append(ToolMessage(content=obs, tool_call_id=t_id))
                else:
                    err = f"Tool '{t_name}' not found."
                    print(f"  ← {err}")
                    messages.append(ToolMessage(content=err, tool_call_id=t_id))

        # ── Final verification ────────────────────────────────────────────
        if os.path.exists(OUTPUT_PATH):
            sz = os.path.getsize(OUTPUT_PATH)
            print(f"[AGENT] ✅ File verified: {OUTPUT_PATH} ({sz} bytes)")
        else:
            print(f"[AGENT] ❌ File MISSING: {OUTPUT_PATH}")

        return {"output": final_output}


# ── CLI entry point ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="?",
                        default="Create a presentation on Artificial Intelligence")
    parser.add_argument("--template", default="corporate_professional")
    parser.add_argument("--slides", type=int, default=5)
    args = parser.parse_args()

    asyncio.run(run_ppt_agent(args.prompt, args.template, args.slides))
