import os
import mcp.server.stdio
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("filesystem-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="save_file",
            description="Saves text content to a local file. Useful for saving research notes or raw markdown before building the PPT.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "The local filename (e.g., 'notes.txt')."},
                    "content": {"type": "string", "description": "The content to save."}
                },
                "required": ["filename", "content"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "save_file":
        filename = arguments.get("filename")
        content = arguments.get("content")
        
        if not filename or not content:
            raise ValueError("Missing filename or content argument")
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            return [TextContent(type="text", text=f"File {filename} successfully saved.")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error saving file: {str(e)}")]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
