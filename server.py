import asyncio

import os

import httpx
from groq import AsyncGroq
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

# Initialize FAstMCP server
mcp = FastMCP("snap4")

# Constants
TPL_BASE_URL = "https://www.snap4city.org/superservicemap/api/v1/tpl"
USER_AGENT = "snap/1.0"
api_key = os.getenv("GROQ_API_KEY")

client = AsyncGroq(api_key=api_key, base_url="https://api.groq.com/")
model = "meta-llama/llama-4-scout-17b-16e-instruct"

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_agencies():
    """
    Calls the endpoint that returns the bus agencies. If the user asks for a specific city or area, look for a correspondence
    in the output of this function.
    """
    url = f"{TPL_BASE_URL}/agencies"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None

@mcp.tool()
async def get_bus_lines(area: str, agency_name: str) -> dict:
    """
    #TODO TO BE REWRITTEN the docstring
    This function returns the BUS LINES that one specific agency operates. The arguments can be either an area (city or region) or the agency name.

    args:
        - area: str, name of a specific zone. It may be a city, it may be a region. In case it is not clear, try to look for clues in the previous conversation.
        - agency_name: str, the name of the agency whose url needs to be retrieved.
    required:
    """
    async def get_agency_url(area: str, agency_name: str, temperature: int = 0, max_tokens=512):
        agencies = await get_agencies()

        get_agency_url_chat_history = [{"role": "system",
                                  "content": "Given this input, give me ONLY the agency link. Answer with 'http' and the correct link. Do not use any other words. The input has either the area or the name of the specific agency. DO NOT WRITE ANYTHING ELSE IN YOUR RESPONSE: ONLY THE AGENCY URL ONCE"
                                  },
                                 {"role": "user", "content": f"Find the link of the agency of tpl that better serves this area: {area}, or look for this specific agency: {agency_name} Use this list: {agencies}"}]

        response = await client.chat.completions.create(
            model=model,  # Adjust the model as necessary
            messages=get_agency_url_chat_history,
            max_tokens=max_tokens,
            temperature=temperature
        )

        return response.choices[0].message.content

    agency =  await get_agency_url(area=area, agency_name=agency_name)
    print(agency)
    url = f"{TPL_BASE_URL}/bus-lines/"
    params = {"agency": agency}
    async with httpx.AsyncClient() as async_client:
        try:
            resp = await async_client.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None


if __name__ == "__main__":
    # Initialize and run the server
    print("\n Server is now running...")
    mcp.run(transport='stdio')

    #res = asyncio.run(get_bus_lines(area="athens", agency_name=""))

    #print(res)
