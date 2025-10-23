import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")
# client = Client("https://psh-test-server.fastmcp.app/mcp")


async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result.structured_content['result'])


async def sum(a: int, b: int):
    async with client:
        result = await client.call_tool("add", {"a": a, "b": b})
        print(result.structured_content['result'])


async def fetch_objects():
    async with client:
        result = await client.call_tool("get_objects", {})
        print(result.structured_content['result'][0])

asyncio.run(call_tool("Saranga"))
# asyncio.run(sum(5, 10))
asyncio.run(fetch_objects())
