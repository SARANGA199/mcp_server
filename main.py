from fastmcp import FastMCP
import httpx
import requests
from urllib.parse import urlencode

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


def get_access_token() -> str:
    url = "https://dev.falkonsms.com/auth/connect/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Postman uses data-urlencode; httpx FormData handles it identically
    data = {
        "grant_type": "client_credentials",
        "scope": "API",
        "client_id": "Client1",
        "Client_secret": "Client1Secret"
    }

    with httpx.Client(verify=True) as client:
        response = client.post(url, data=data, headers=headers)
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)

        if response.status_code != 200:
            raise Exception(f"Failed to get access token: {response.text}")

        token_data = response.json()
        return token_data["access_token"]


@mcp.tool
def send_sms(ToPhoneNumber: str, Body: str) -> str:
    """
    Sends an SMS message using Falkon SMS API.
    - ToPhoneNumber: Recipient phone number
    - Body: Message content
    """
    try:
        # Step 1: Get access token
        access_token = get_access_token()

        # Step 2: Send SMS
        url = "https://dev.falkonsms.com/be-api/api/Messages/Send"
        headers = {
            "Accept": "text/plain",
            "PhoneNumber": "+12407461350",
            "PhoneNumberId": "7b236508-634f-4d03-9676-fdf888f35c29",
            "Authorization": f"Bearer {access_token}",
            "GroupId": "0",
            "Provider": "Bandwidth",
            "OrgReference": "FBE3",
            "OrganizationId": "5f9ea413-2c36-4826-98db-fc7b46b8186c",
            "UserId": "64476efb-e665-4ff6-ae40-f391023ff725"
        }

        # form-data encoding using 'files'
        files = {
            "Body": (None, Body),
            "ToPhoneNumber": (None, ToPhoneNumber),
            "Credits": (None, "1"),
            "SequenceId": (None, "")
        }

        with httpx.Client() as client:
            response = client.post(url, headers=headers, files=files)

        if response.status_code == 200:
            return f"✅ Message sent successfully to {ToPhoneNumber}"
        else:
            return f"❌ Failed to send message: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error occurred: {str(e)}"


if __name__ == "__main__":
    mcp.run()
