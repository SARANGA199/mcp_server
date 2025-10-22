import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")


async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result.structured_content['result'])


async def sum(a: int, b: int):
    async with client:
        result = await client.call_tool("add", {"a": a, "b": b})
        print(result.structured_content['result'])

asyncio.run(call_tool("Saranga"))
asyncio.run(sum(5, 10))
