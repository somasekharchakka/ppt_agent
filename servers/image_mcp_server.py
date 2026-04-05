import os
from PIL import Image, ImageDraw, ImageFont
import mcp.server.stdio
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("image-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="generate_placeholder_image",
            description="Generates a placeholder image and saves it locally. Used to prepare assets before inserting them into a PPT.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Local filename to save the image to (e.g., 'star.png')."},
                    "prompt": {"type": "string", "description": "The textual description to embed in the placeholder image."}
                },
                "required": ["filename", "prompt"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "generate_placeholder_image":
        filename = arguments.get("filename")
        prompt = arguments.get("prompt", "Placeholder")
        
        if not filename:
            raise ValueError("Missing filename argument")
            
        try:
            # Create a simple solid color image
            img = Image.new('RGB', (800, 600), color = (73, 109, 137))
            d = ImageDraw.Draw(img)
            # Add text
            d.text((50, 300), prompt, fill=(255,255,255))
            
            img.save(filename)
            return [TextContent(type="text", text=f"Successfully generated placeholder image to {filename} with prompt: {prompt}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error generating image: {str(e)}")]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
