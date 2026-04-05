import wikipedia
import mcp.server.stdio
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("search-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_wikipedia",
            description="Searches Wikipedia for accurate data on a given topic to use in presentations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."}
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_wikipedia":
        query = arguments.get("query")
        if not query:
            raise ValueError("Missing query argument")
        
        try:
            results = wikipedia.summary(query, sentences=3)
            return [TextContent(type="text", text=results)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error searching wikipedia: {str(e)}")]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
