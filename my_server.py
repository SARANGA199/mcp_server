from fastmcp import FastMCP
import requests

mcp = FastMCP("My MCP Server")


@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"


@mcp.tool
def add(a: int, b: int) -> int:
    return a + b

# -------------------------------
# New Tool: Fetch Object Details
# -------------------------------


@mcp.tool
def get_objects() -> dict:
    """
    Fetches data from the public RESTful API (https://api.restful-api.dev/objects)
    and returns it under the key 'result' for compatibility.
    """
    try:
        response = requests.get(
            "https://api.restful-api.dev/objects", timeout=10)
        response.raise_for_status()
        data = response.json()
        return {"result": data}  # ✅ Put data under 'result'
    except requests.RequestException as e:
        return {"result": f"Error fetching data: {e}"}


if __name__ == "__main__":
    mcp.run()
