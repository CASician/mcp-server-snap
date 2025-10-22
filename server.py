import asyncio

import os

import httpx
from groq import AsyncGroq
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# Initialize FAstMCP server
mcp = FastMCP("snap4")

# Constants
TPL_BASE_URL = "https://www.snap4city.org/superservicemap/api/v1/"
USER_AGENT = "snap/1.0"
api_key = os.getenv("GROQ_API_KEY")

client = AsyncGroq(api_key=api_key, base_url="https://api.groq.com/")
model = "meta-llama/llama-4-scout-17b-16e-instruct"

@mcp.resource("file://snap/agencies")
async def get_agencies():
    """
    Returns the bus agencies. If the user asks for a specific city or area, look for a correspondence
    in the output of this function.
    """
    url = f"{TPL_BASE_URL}/tpl/agencies"

    """
    [NOTA PER LA TESI]
    Chiamare l'endpoint non credo sia ideale per queste situazioni. Idealmente vorrei farlo una volta al giorno/settimana.
    Il risultato lo salvo in un file a parte e questa funzione legge quel file. 
    Per aggiornare quel file creerei un tool (disponibile anche al client) che gira sul server e aggiorna il file con regolarità
    Stessa cosa vale per tutti gli altri mcp.resources
    """
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None

@mcp.tool()
async def get_events(
    range: Optional[str],
    selection: Optional[str],
    maxDists: Optional[float],
    maxResults: Optional[int] 
):
    """
    It allows to retrieve the geolocated events in a given temporal range (day, week or month). 
    The results can be possibly filtered to be within a specified distance from a GPS position, or within a rectangular area or inside a WKT described geographic area.

    args:
        - range: str, Time range for the events to be retrieved, it can be day for the events of the day of the request, week for the events in the next 7 days or month for the events in the next 30 days (if omitted day is assumed).
        - selection: str, Optional lat;lng with a GPS position, or lat1;lng1;lat2;lng2 for a rectangular area or wkt:string or geo:geoid for a geographic area described as Well Known Text (see other request types for more details). Example: 43.7756;11.2490
        - maxDists: float, Maximum distance from the reference position (selection parameter), expressed in kilometers. This parameter can also be set to inside, in which case services are discovered that have a WKT geometry that covers the reference position. It defaults to 0.1. Example: 0.2
        - maxResults: int, Maximum number of results to be returned. If it is set to zero, all results are returned. It defaults to 100. Example: 10
    """
    
    url = f"{TPL_BASE_URL}/events"
    params = {}
    for key, value in {
        "range": range,
        "selection": selection,
        "maxDists": maxDists,
        "maxResults": maxResults,
    }.items():
        if value is not None:
            params[key] = value



    async with httpx.AsyncClient() as async_client:
        try:
            resp = await async_client.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None




@mcp.tool()
async def get_bus_lines(area: str, agency_name: str) -> dict:
    """
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
    url = f"{TPL_BASE_URL}/tpl/bus-lines/"
    params = {"agency": agency}
    async with httpx.AsyncClient() as async_client:
        try:
            resp = await async_client.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None


@mcp.prompt("explain_bus_lines")
async def explain_bus_lines_prompt(bus_data: dict, area: str = None):
    """
    Generate a natural-language explanation for the bus lines available in a given area.

    Args:
        bus_data (dict): The JSON returned by get_bus_lines().
        area (str, optional): The name of the area to contextualize the answer.
    """
    intro = f"The following is the list of bus lines operating in {area}:" if area else "Here are some bus lines:"

    # This prompt simply structures what the model should do with the JSON data
    return {
        "role": "system",
        "content": (
            f"{intro}\n\n"
            f"{bus_data}\n\n"
            "Please explain to the user in a clear and friendly way:\n"
            "- How many lines there are,\n"
            "- Which ones seem to be the main routes (based on names or codes),\n"
            "- And any pattern you can infer (e.g. which cover the city center or suburbs).\n"
            "Avoid restating the raw JSON; focus on clarity and usefulness."
        )
    }

if __name__ == "__main__":
    # Initialize and run the server
    print("\n Server is now running...")
    mcp.run(transport='stdio')

    #res = asyncio.run(get_bus_lines(area="athens", agency_name=""))

    #print(res)
