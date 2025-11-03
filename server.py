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
TPL_BASE_URL = "https://www.snap4city.org/superservicemap/api/v1"
USER_AGENT = "snap/1.0"
api_key = os.getenv("GROQ_API_KEY")

client = AsyncGroq(api_key=api_key, base_url="https://api.groq.com/")
model = "meta-llama/llama-4-scout-17b-16e-instruct"

# ------------------------ SERVICES ------------------------

@mcp.tool()
async def get_services(
        selection: Optional[str] = None,
        queryId: Optional[str] = None,
        search: Optional[str] = None,
        categories: Optional[str] = None,
        text: Optional[str] = None,
        maxDists: Optional[str] = None,
        maxResults: Optional[str] = None,
        lang: Optional[str] = None,
        geometry: Optional[str] = None,
        uid: Optional[str] = None,
        format: Optional[str] = None,
        map: Optional[str] = None,
        controls: Optional[str] = None,
        info: Optional[str] = None,
        serviceUri: Optional[str] = None,
        realtime: Optional[str] = None,
        requestFrom: Optional[str] = None,
        valueName: Optional[str] = None,
        fromTime: Optional[str] = None,
        toTime: Optional[str] = None,
        value_type: Optional[str] = None,
        healthiness: Optional[str] = None,
        graphUri: Optional[str] = None,
        fullCount: Optional[str] = None,
        accessToken: Optional[str] = None,
        apikey: Optional[str] = None
):
    """
    Service search near GPS position - It allows to retrieve the set of services that are near a given GPS position. The services can be filtered as belonging to specific categories (e.g. Accommodation, Hotel, Restaurant, etc.), or having specific words in any textual field. It can also be used to find services that have a WKT spatial description that contains a specific GPS position.
    Service search near a service - It allows to retrieve the set of services that are near a given service identified by its serviceUri. The services can be filtered as belonging to specific categories (e.g. Accommodation, Hotel, Restaurant, etc.), or having specific words in any textual field. It can also be used to find services that have a WKT spatial description that contains a specific GPS position.
    Service search within a GPS area - It allows to retrieve the set of services that are inside a rectangular area. The services can be filtered as belonging to specific categories (e.g. Accommodation, Hotel, Restaurant, etc.), or having specific words in any textual field.
    Service search within a WKT described area - It allows to retrieve the set of services that are inside a geographic region described using the Well Known Text (WKT) format. The services can be filtered as belonging to specific categories (e.g. Accommodation, Hotel, Restaurant, etc.), or having specific words in any textual field.
    Service search within a stored WKT described area - It allows to retrieve the set of services that are inside a geographic region described using the Well Known Text (WKT) format, by referring to the WKT with an identifier provided when the WKT is stored. The services can be filtered as belonging to specific categories (e.g. Accommodation, Hotel, Restaurant, etc.), or having specific words in any textual field. The list of available geometries can be retrieved from the Service Map in the Search Area selection box (with Search Range specific area). New geometries can be provided using the http://www.km4city.org/wkt web service which can store a WKT from a shp file or providing directly the WKT string.
    Service search by municipality - It allows to retrieve the set of services that are in a specific municipality. The services can be filtered as belonging to specific categories (e.g. Accommodation, Hotel, Restaurant, etc.), or having specific words in any textual field.
    Service search by query id - It allows to retrieve the set of services associated with a query stored using the Service Map user interface.
    Full text search - It allows to retrieve the geolocated entities (not only services) that match with a list of keywords. The results can be possibly filtered to be within a specified distance from a GPS position, or within a rectangular area or inside a WKT geolocated area.
    Service info - It allows to retrieve information about a service using its serviceUri, as an HTML (format query parameter set to html) or a machine-readable JSON document (format query parameter set to json).

    args:
        - selection: str, Through this parameter, the user indicates where the services have to be searched. It could be a boundary within which to search, or a point around which to search.
                    Usages & Sample values:
                    Service search near GPS position - WGS84 sessadecimal representation of the latitude and longitude of the position of interest, separated by a semicolon. Required. Sample value: 43.7756;11.2490.
                    Service search near a service - Service search near a service. Required. Sample value: http://www.disit.org/km4city/resource/7ad6d2d3be461b1f0514956279c00eab
                    Service search within a GPS (rectangular) area - Lat#1;Lon#1;Lat#2;Lng#2 where Lat#1;Lng#1 are the WGS84 sessadecimal coordinates of the south-west point of the rectangle, and Lat#2;Lng#2 are the coordinates of the north-east point. Required. Sample value: 3.7741;11.2453;43.7768;11.2515
                    Service search within a WKT described area - wkt:string describes the geographic region as WKT string. Required. Sample value: wkt:POLYGON((11.25539 43.77339, 11.25608 43.77348, 11.25706 43.77362, 11.25759 43.77328, 11.25755 43.77291, 11.25675 43.77260, 11.25536 43.77270, 11.25539 43.77339))
                    Service search within a stored WKT described area - geo:geo_id where geo_id identifies a WKT string stored on the server. Required. Sample value: geo:ritmi_01
                    Service search by municipality - Name of the municipality like FIRENZE, EMPOLI, PISA possibly with prefix "COMUNE di". Required. Sample value: COMUNE di FIRENZE
                    Full text search - Optional lat;lng with a GPS position, or lat1;lng1;lat2;lng2 for a rectangular area or wkt:string or geo:geoid for a geographic area described as Well Known Text (see other request types for more details). Sample value: via dell'artigianato

        - queryId: str, Identifier of the query stored on servicemap.
                    Usage: Service search by query id
                    Example: e02db54355fea40808300473c3537ff
        - search: str, The keywords separated by spaces that have to match with any textual description associated with an entity. Required.
                    Usage: Full text search (Required)
                    Example: via nave
        - categories: str, The list of categories of the services to be retrieved separated with semicolon, if omitted all kinds of services are returned. It can contain macro categories or categories, if a macro category is specified all categories in the macro category are used. The complete list of categories and macro categories can be retrieved on servicemap.disit.org.
                    Usages:
                    Service search near GPS position
                    Service search near a service
                    Service search within a GPS area
                    Service search within a WKT described area
                    Service search within a stored WKT described area
                    Service search by municipality
        - text: str, Words in this parameter are used to retrieve services that contain all these words in any textual description associated with the service.
                    Usages:
                    Service search near GPS position
                    Service search near a service
                    Service search within a GPS area
                    Service search within a WKT described area
                    Service search within a stored WKT described area
                    Service search by municipality
                    Example: casa di dante
        - maxDists: float?
                    Maximum distance from the reference position (selection parameter), expressed in kilometers. This parameter can also be set to inside, in which case services are discovered that have a WKT geometry that covers the reference position. It defaults to 0.1.
                    Usages:
                    Service search near GPS position
                    Service search near a service
                    Full text search
                    Default value : 0.1
        - maxResults: int
                    Maximum number of results to be returned. If it is set to zero, all results are returned. It defaults to 100.
                    Usages:
                    Service search near GPS position
                    Service search near a service
                    Service search within a GPS area
                    Service search within a WKT described area
                    Service search within a stored WKT described area
                    Service search by municipality
                    Full text search
                    Default value : 100
        - lang: str,
                    ISO 2 chars language code (e.g. it, en, fr, de, es, etc. ) to be used for service descriptions. For that localized descriptions could be provided, they must be available in the Knowledge Base. No on-the-fly translation is performed. If a description is not available in the requested language, or if the parameter cannot be found in the input query, the English description is returned.
                    Usages:
                    Service search near GPS position
                    Service search near a service
                    Service search within a GPS area
                    Service search within a WKT described area
                    Service search within a stored WKT described area
                    Service search by municipality
                    Service search by query id
                    Full text search
                    Service info
                    Default value : en
        - geometry: bool
                    If it is set to true, the hasGeometry property is returned for each service, that describes whether the service has a complex WKT geometry (linestring, polygon) or not. It defaults to false.
                    Usages:
                    Service search near GPS position
                    Service search near a service
                    Service search within a GPS area
                    Service search within a WKT described area
                    Service search within a stored WKT described area
                    Service search by municipality
                    Service search by query id
                    Full text search
                    Example: true
                    Default value : false
        - uid: str
                    Optional user identifier.
                    Usages:
                    Service search near GPS position
                    Service search near a service
                    Service search within a GPS area
                    Service search within a WKT described area
                    Service search within a stored WKT described area
                    Service search by municipality
                    Service search by query id
                    Full text search
                    Service info
                    Example: e7c13b5ce309dcddce9f72c810c3f93c61ac1c47d66126127f7a78bd5c2cb8a2
        - format: str
                    Output format: html, or json. It defaults to json.
                    Usages:
                    Service search near GPS position
                    Service search near a service
                    Service search within a GPS area
                    Service search within a WKT described area
                    Service search within a stored WKT described area
                    Service search by municipality
                    Service search by query id
                    Full text search
                    Service info
                    Available values : html, json
                    Default value : json
        - map: str
                    The type of map to be used (i.e. satellite, streets or grayscale).
                    Usage: All requests where the output format is set to html
                    Example: satellite
                    Available values : satellite, streets, grayscale
        - controls:
                    Hides or collapses the controls on the left and right sides of the Web page. It can be set to hidden or false to hide them, and to collapsed to collapse them.
                    Usage: All requests where the output format is set to html
                    Example: hidden
        - info:
                    Hides or collapses the info tab in the bottom left corner of the Web page. It can be set to hidden or false to hide it, and to collapsed to collapse it.
                    Usage: All requests where the output format is set to html
                    Example: collapsed
        - serviceUri:
                    URI of the service of interest. Required.
                    Usages: Service info
                    Example: http://www.disit.org/km4city/resource/RT04801702315PO
        - realtime:
                    It indicates if the last values of the time varying properties should be provided in the result or not. It defaults to true.
                    Usages: Service info
                    Example: false
                    Default value : true
        - requestFrom: str, The parameter identifies the request's originator for monitoring purposes.
        - valueName: str, To be used in requests for real-time values, to retrieve only the value of interest among the set of the available real-time values.
        - fromTime:str, To be used in requests for real-time values, to indicate the date and time of start of the time interval of interest.
        - toTime: str, To be used in requests for real-time values, to indicate the date and time of end of the time interval of interest.
        - value_type: str, To be used in requests for real-time values, to retrieve only values of the given type.
        - healthiness: bool, The parameter allows to filter results by healthiness
        - graphUri: str, To indicate the URI of the graph where resources have to be looked for.
        - fullCount: bool, To indicate whether the full count of the retrieved resources have to be computed and provided back, or not. If set to false, an improvement in performances can be observed
        - accessToken: str, The parameter allows to perform authenticated requests, and therefore retrieve not only public data, but also private data that is owned or delegated to the user associated with the specified access token
        - apikey: str, The parameter identifies the request's originator for monitoring/authorization purposes.

    You need to specify at least one from 'selection', 'search', 'serviceUri' or 'queryId' parameters.

    :return:

    """
    url = f"{TPL_BASE_URL}"
    params = {}
    for key, value in {
            "selection": selection,
            "queryId": queryId,
            "search": search,
            "categories": categories,
            "text": text,
            "maxDists": maxDists,
            "maxResults": maxResults,
            "lang": lang,
            "geometry": geometry,
            "uid": uid,
            "format": format,
            "map": map,
            "controls": controls,
            "info": info,
            "serviceUri": serviceUri,
            "realtime": realtime,
            "requestFrom": requestFrom,
            "valueName": valueName,
            "fromTime": fromTime,
            "toTime": toTime,
            "value_type": value_type,
            "healthiness": healthiness,
            "graphUri": graphUri,
            "fullCount": fullCount,
            "accessToken": accessToken,
            "apikey": apikey
    }.items():
        if value:
            params[key] = value

    async with httpx.AsyncClient() as async_client:
        try:
            resp = await async_client.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None
# ------------------------ IOT SEARCH --------------------------------

@mcp.tool()
async def iot_search(
        selection: Optional[str] = None,
        maxDists: Optional[str] = None,
        categories: Optional[str] = None,
        model: Optional[str] = None,
        valueFilters: Optional[str] = None,
        serviceUri: Optional[str] = None,
        text: Optional[str] = None,
        notHealthy: Optional[str] = None,
        fromResult: Optional[str] = None,
        maxResults: Optional[str] = None,
        values: Optional[str] = None,
        sortOnValue: Optional[str] = None,
):
    """
    This API allows to search over services submitted as IOT devices. The main characteristic is that it can search for devices whose last values satisfy specific conditions, for example it allows to find all Weather_sensor devices in a geographic area whose last value of temperature is over 30 degrees.
    The results can be filtered to be within a specified distance from a GPS position, or within a rectangular area (wkt polygonal area query is not supported).
    Moreover, results can be filtered by the model used in IoT Directory to create the device, categories (nature or subnature) associated to the device, valueFilters reporting conditions (in AND) on the last value received for dynamic attributes (e.g. status:Active;temperature>=23). The results can be paged using fromResult/maxResults.
    Normally only public iot devices are returned, if you want to include private devices (your own or delegated to you) you have to send an access token in the Authorization header or using the accessToken query parameter.
    Data is indexed on elasticsearch only after any update on the context broker, thus if you change ownership or add a delegation on the device it will be applied only after a data update.
    Consider that the device status is updated on every device change on the context broker, thus if updates are made out of time order it is not guaranteed that the device status provided is the most recent
    Always specify 'selection' or 'model' or 'valueFilters' or 'categories' or 'serviceUri' parameter.
    When you need to pass a number to the function, pass it as an int or float, do not use semi colons.
    Also when you don't use a parameter, call the function without that parameter. Do not pass an empty string.
    args:
        - selection: str, Through this parameter, the user indicates where the services have to be searched. It could be a rectangular boundary within which to search, or a point around which to search.
                        Usages & Sample values:
                        - Service search near GPS position - WGS84 sessadecimal representation of the latitude and longitude of the position of interest, separated by a semicolon. Required. Sample value: 43.7756;11.2490.
                        - Service search near a service - Service search near a service. Required. Sample value: http://www.disit.org/km4city/resource/7ad6d2d3be461b1f0514956279c00eab
                        - Service search within a GPS (rectangular) area - Lat#1;Lon#1;Lat#2;Lng#2 where Lat#1;Lng#1 are the WGS84 sessadecimal coordinates of the south-west point of the rectangle, and Lat#2;Lng#2 are the coordinates of the north-east point. Required. Sample value: 43.7741;11.2453;43.7768;11.2515
        - maxDists: number, maximum distance in km from the GPS point specified with selection in the form "lat;lon" (default 0.1)
        - categories: str, A list of categories as nature or subnature separated with ";"
        - model: str, search for iot devices created with a specific model name
        - valueFilters: str, a list of conditions (separated with ;) on value names matching a constant value. The matching operator can be:
                        value name=numeric value (e.g. temperature=18), search for devices having the dynamic numeric attribute "value name" with a specific numeric value.
                        value name>numeric value (e.g. temperature>20), search for devices having a dynamic numeric attribute greater than a specific value.
                        value name>=numeric value (e.g. temperature>=20), search for devices having a dynamic numeric attribute greater or equal than a specific value.
                        value name<numeric value (e.g. temperature<20), search for devices having a dynamic numeric attribute less than a specific value.
                        value name<=numeric value (e.g. temperature<=20), search for devices having a dynamic numeric attribute less or equal than a specific value.
                        value name:string value (e.g. status:Active), search for devices having the dynamic string attribute "value name" with a specific value, the match is case-sensitive
                        value name!:string value (e.g. status!:Active), search for devices having a dynamic string attribute different from a specific value.
                        value name:>string value (e.g. status:>Act), search for devices having a dynamic string attribute greater than a specific string value.
                        value name:>=string value (e.g. status:>=Active), search for devices having a dynamic string attribute greater or equal than a specific value.
                        value name:<string value (e.g. status:<A), search for devices having a dynamic string attribute less than a specific value.
                        value name:<=string value (e.g. status:<=Active), search for devices having a dynamic string attribute less or equal than a specific value.
                        If multiple conditions are present they are considered in AND.
                        The special value name "deviceDelay_s" contains the number of seconds elapsed since last data update, it can be used to search for devices that does not send data since a certain number of seconds (to find unhealthy devices) or to find only recently updated devices.
        - serviceUri: str, Through this parameter, the user indicates a list of serviceUri (separated by ;) to be returned, this filter is used in conjuncion with the other filters.
        - text: str, Through this parameter, the user indicates a set of keywords or phrases delimited with " to be matched on any device value.
        - notHealthy: str, Through this parameter, the user indicates to return only not healthy devices if "true" is specified (default false). Not healthy devices are identified computing at update time the time expected for next update, not healthy devices are those whose value of this time is before current time (a configurable threshold of 1 minute is used).
        - fromResult: number, the first result to be returned (default 0)
        - maxResults: number, number of results to be returned (default 100)
        - values: str, list of value names (separated by ;) to be returned for each result, if omitted all values are returned
        - sortOnValue: str, the value name to sort the result, it can be like "value name:asc|desc:type" (e.g. temperature:desc:short), order direction is "asc" if omitted, type can be string, date, long or short (if type is omitted string is assumed). The type is used to force sorting for dates and numbers. If the parameter is omitted the sort is on the distance from GPS position, if "none" is specified no specific sort is used. If "deviceDelay_s:desc" is specified results are sorted on the delay time in seconds passed from the last value provided for the device, in this way
    :return:
    """
    url = f"{TPL_BASE_URL}/iot-search"
    params = {}
    for key, value in {
        "selection": selection,
        "maxDists": maxDists, # float
        "categories": categories,
        "model": model,
        "valueFilters": valueFilters,
        "serviceUri": serviceUri,
        "text": text,
        "notHealthy": notHealthy,
        "fromResult": fromResult, # int con quello sotto.
        "maxResults": maxResults,
        "values": values,
        "sortOnValue": sortOnValue
    }.items():
        if value:
            params[key] = value

    async with httpx.AsyncClient() as async_client:
        try:
            resp = await async_client.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None

@mcp.tool()
async def iot_search_time_range(
        fromTime: Optional[str] = None,
        toTime: Optional[str] = None,
        selection: Optional[str] = None,
        maxDists: Optional[str] = None,
        categories: Optional[str] = None,
        model: Optional[str] = None,
        valueFilters: Optional[str] = None,
        serviceUri: Optional[str] = None,
        text: Optional[str] = None,
        fromResult: Optional[str] = None,
        maxResults: Optional[str] = None,
        aggregate: Optional[str] = None,
        values: Optional[str] = None,
        sortOnValue: Optional[str] = None,
):
    """
    IoT device/value search over a time range
    This API allows to search over services submitted as IOT devices. The main characteristic is that it can search for devices whose values satisfy specific conditions in a certain time range, for example it allows to find all Weather_sensor devices in a geographic area whose value of temperature is over 30 degrees at least one time over last week. But this api can return all the temporal values matching the request (in this case a service uri is repeated as many times as it matches the query in the time range)
    The results can be filtered to be within a specified distance from a GPS position, or within a rectangular area (wkt polygonal area query is not supported).
    Moreover, results can be filtered by the model used in IoT Directory to create the device, categories (nature or subnature) associated to the device, valueFilters reporting conditions (in AND) on the last value received for dynamic attributes (e.g. status:Active;temperature>=23).
    The results can be aggregated by service uri with aggregation=true if data is not aggregated can be paged using fromResult/maxResults.
    Normally only public iot devices are returned, if you want to include private devices (your own or delegated to you) you have to send an access token in the Authorization header or using the accessToken query parameter.
    Data is indexed on elasticsearch, consider that ownership and delegations are not updated for old data, so if ownership or delegations of a device are modified at a certain point in time this api will provide to the new owner or delegated user only data submitted after this change.
    Specify at least 'selection' or 'model' or 'valueFilter' or 'categories' or 'serviceUri' parameter.
    Also specify fromTime
    args:
    - fromTime: str, expected n-day,n-hour,n-minute or yyyy-mm-ddThh:mm:ss
    - toTime: str,
    - selection: str,
    - maxDists: float,
    - categories: string,
    - model: string,
    - valueFilters: str,
    - serviceUri: str,
    - text: str,
    - fromResult: float,
    - maxResults: int,
    - aggregate: str,
    - values: str,
    - sortOnValue: str,

    :return:
    """
    url = f"{TPL_BASE_URL}/iot-search/time-range/"
    params = {}
    for key, value in {
        "fromTime": fromTime,
        "toTime": toTime,
        "selection": selection,
        "maxDists": maxDists,
        "categories": categories,
        "model": model,
        "valueFilters": valueFilters,
        "serviceUri": serviceUri,
        "text": text,
        "fromResult": fromResult,
        "maxResults": maxResults,
        "aggregate": aggregate,
        "values": values,
        "sortOnValue": sortOnValue
    }.items():
        if value:
            params[key] = value

    async with httpx.AsyncClient() as async_client:
        try:
            resp = await async_client.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None

# ------------------------ EVENTS ------------------------

# Does it work in snap? Is it used?
@mcp.tool()
async def get_events(
        range: Optional[str] = None,
        selection: Optional[str] = None,
        maxDists: Optional[str] = None,
        maxResults: Optional[str] = None
):
    """
    It allows to retrieve the geolocated events in a given temporal range (day, week or month).
    The results can be possibly filtered to be within a specified distance from a GPS position, or within a rectangular area or inside a WKT described geographic area.

    args:
        - range: str, Time range for the events to be retrieved, it can be day for the events of the day of the request, week for the events in the next 7 days or month for the events in the next 30 days (if omitted day is assumed).
        - selection: str, Optional lat;lng with a GPS position, or lat1;lng1;lat2;lng2 for a rectangular area or wkt:string or geo:geoid for a geographic area described as Well Known Text (see other request types for more details). Example: 43.7756;11.2490
        - maxDists: float, Maximum distance from the reference position (selection parameter), expressed in kilometers. This parameter can also be set to inside, in which case services are discovered that have a WKT geometry that covers the reference position. It defaults to 0.1. Example: 0.2
        - maxResults: int, Maximum number of results to be returned. If it is set to zero, all results are returned. It defaults to 100. Example: 10

    :return: json
    """

    url = f"{TPL_BASE_URL}/events"
    params = {}
    for key, value in {
        "range": range,
        "selection": selection,
        "maxDists": maxDists,
        "maxResults": maxResults,
    }.items():
        if value:
            params[key] = value

    async with httpx.AsyncClient() as async_client:
        try:
            resp = await async_client.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None


# ------------------------ LOCATIONS ------------------------

@mcp.tool()
async def get_location(
        position: str,
        search: Optional[str] = None,
        searchMode: Optional[str] = None,
        maxDists: Optional[str] = None,
        excludePOI: Optional[str] = None,
        maxResults: Optional[str] = None,
        intersectGeom: Optional[str] = None,
        uid: Optional[str] = None,
        requestFrom: Optional[str] = None
):
    """
    Address and geometry search by GPS It allows to retrieve the complete address (municipality, street and civic number) given the GPS position. It may also provide a list of services or public transport lines intersecting with the provided GPS position.
    Address/POI search by text It allows to retrieve a list of street addresses and service names based on a text search. The search may be filtered excluding POIs and to be within a maximum distance from a GPS position.
    Specify at least 'position' or 'search' parameters.
    args:
        - position: str, The position of interest, identified through a pair of WGS84 coordinates, latitude and longitude, separated by a semicolon. Required.
                    Usages: Address and geometry search by GPS (Required), Address/POI search by text (Optional)
        - search: str, A text with the words to be found in the names of the streets, civic number, municipality names and service names. Required.
                    Usages: Address/POI search by text
                    Example: via calzaioli
        - searchMode: str, Optional can be AND or ANDOR (default ANDOR), indicates if all or any word of the query need to match.
                    Usages: Address/POI search by text
                    Example: AND
                    Available values : AND, ANDOR
                    Default value : ANDOR
        - maxDists: float, Optional maximum distance in km from position for searching the text (if omitted 5 km is assumed).
                    Usages: Address/POI search by text
                    Example: 10
                    Default value : 5
        - excludePOI: bool, Optional true or false (assumed false if missing), if true the search is performed only on street names, civic numbers and municipalities.
                    Usages: Address/POI search by text
                    Example: true
                    Default value : false
        - maxResults: int, Optional maximum number of results provided (default 10).
                    Usages: Address/POI search by text
                    Example: 20
                    Default value : 10
        - intersectGeom: bool, True or false (assumed false if missing), if true it reports all the services and public transportation lines that have a geometry intersecting with the provided GPS position.
                    Usages: Address/POI search by GPS
                    Example: true
                    Default value : false
        - uid: str, Optional user identifier.
                    Usages: Address and geometry search by GPS, Address/POI search by text.
                    Example: e7c13b5ce309dcddce9f72c810c3f93c61ac1c47d66126127f7a78bd5c2cb8a2
        - requestFrom: str, The parameter identifies the request's originator for monitoring purposes.
    required:
        - position
    :return:
    """
    url = f"{TPL_BASE_URL}/location"
    params = {}
    for key, value in {
        "position": position,
        "search": search,
        "searchMode": searchMode,
        "maxDists": maxDists,
        "excludePOI": excludePOI,
        "maxResults": maxResults,
        "intersectGeom": intersectGeom,
        "uid": uid,
        "requestFrom": requestFrom,
    }.items():
        if value:
            params[key] = value

    async with httpx.AsyncClient() as async_client:
        try:
            resp = await async_client.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None


# ------------------------ PUBLIC TRANSPORT ------------------------

@mcp.resource("file://snap/agencies")
# SPERIMENTALE
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
# SPERIMENTALE
async def get_bus_lines(area: str, agency_name: str) -> dict:
    """
    This function returns the BUS LINES that one specific agency operates. The arguments can be either an area (city or region) or the agency name.

    args:
        - area: str, name of a specific zone. It may be a city, it may be a region. In case it is not clear, try to look for clues in the previous conversation.
        - agency_name: str, the name of the agency whose url needs to be retrieved.
    required:
        - area, default "Firenze"
        - agency_name, default "AT Autolinee Toscane"
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

@mcp.tool()
async def get_bus_routes(
        agency: Optional[str] = None,
        line: Optional[str] = None,
        busStopName: Optional[str] = None,
        geometry: Optional[str] = None,
        uid: Optional[str] = None,
        requestFrom: Optional[str] = None,
):
    """
    The API provides a list of the public transport routes available for a given agency, line or passing by a specific stop.
    You need al least 'line' or 'busStopName' or 'agency' parameters.
    args:
        - agency: str, URI of the agency whose lines are to be retrieved
        - line: str, URI or shortName of a line (if URI is provided the agency is not needed).
        - busStopName: str, URI or name of a stop (if URI is provided the agency is not needed).
                    Example: Stazione Pensilina
        - geometry: bool, If true the WKT geometry of the route is returned (false is assumed if not provided).
        - uid: str, Optional user identifier.
                    Example: e7c13b5ce309dcddce9f72c810c3f93c61ac1c47d66126127f7a78bd5c2cb8a2
        - requestFrom: str, The parameter identifies the request's originator for monitoring purposes
    :return: 
    """
    url = f"{TPL_BASE_URL}/tpl/bus-routes/"
    params = {}
    for key, value in {
        "agency": agency,
        "line": line,
        "busStopName": busStopName,
        "geometry": geometry,
        "uid": uid,
        "requestFrom": requestFrom
    }.items():
        if value:
            params[key] = value

    async with httpx.AsyncClient() as async_client:
        try:
            resp = await async_client.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None


@mcp.tool()
async def get_bus_stops(
        route: Optional[str] = None,
        geometry: Optional[str] = None,
        uid: Optional[str] = None,
        requestFrom: Optional[str] = None,
):
    """
    The API provides a list of the public transport stops available for a given route. The API can be used on any kind of public transport (Tram, Train, etc.) not only Bus.

    args:
        - route: str, URI of the route whose bus stops are to be retrieved
        - geometry: bool, If true, the WKT geometry of the route is returned. It defaults to true.
                    Default value : true
        - uid: string, Optional user identifier.
                    Example: e7c13b5ce309dcddce9f72c810c3f93c61ac1c47d66126127f7a78bd5c2cb8a2
        - requestFrom: string, The parameter identifies the request's originator for monitoring purposes.
    :return:
    """
    url = f"{TPL_BASE_URL}/tpl/bus-stops/"
    params = {}
    for key, value in {
        "route": route,
        "geometry": geometry,
        "uid": uid,
        "requestFrom": requestFrom
    }.items():
        if value:
            params[key] = value

    async with httpx.AsyncClient() as async_client:
        try:
            resp = await async_client.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None

@mcp.tool()
async def tpl_geo_search(
        selection: str,
        maxDists: Optional[str] = None,
        maxResults: Optional[str] = None,
        agency: Optional[str] = None,
        geometry: Optional[str] = None,
        uid: Optional[str] = None,
        requestFrom: Optional[str] = None,
):
    """
    The API provides a list of the public transport routes that have a stop in a specified area. The API can be used on any kind of public transport (Tram, Train, etc.) not only Bus.

    args:
        - selection: str, Valid valorizations:
                    WGS84 coordinates that identify an exact GPS position: lat;lng
                    rectangular area: lat1;lng1;lat2;lng2
                    geographic area described as Well Known Text: wkt:string or geo:geoid
                    See the selection parameter of Services API for further details.
        - maxDists: float, Optional maximum distance from the GPS position of the entities to be retrieved, expressed in Km (0.1 is assumed if not present).
                    Default value : 0.1
        - maxResults: int, Maximum number of results to be returned (if parameter is missing 100 is assumed), if it is 0 all results are returned.
                    Default value : 100
        - agency: str, Optional URI of an agency to restrict the search to a specified agency.
                    Example: http://www.disit.org/km4city/resource/Bus_ataflinea_Agency_172
        - geometry: bool, If true, the WKT geometry of each route is returned (considered false if not provided).
                    Default value : false
        - uid: str, Optional user identifier.
                    Example: e7c13b5ce309dcddce9f72c810c3f93c61ac1c47d66126127f7a78bd5c2cb8a2
        - requestFrom: str, The parameter identifies the request's originator for monitoring purposes.
    required:
        - selection
    :return:
    """
    url = f"{TPL_BASE_URL}/tpl"
    params = {}
    for key, value in {
        "selection": selection,
        "maxDists": maxDists,
        "maxResults": maxResults,
        "agency": agency,
        "geometry": geometry,
        "uid": uid,
        "requestFrom": requestFrom
    }.items():
        if value:
            params[key] = value

    async with httpx.AsyncClient() as async_client:
        try:
            resp = await async_client.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None

@mcp.tool()
async def get_bus_position(
        agency: Optional[str] = None,
        line: Optional[str] = None,
        uid: Optional[str] = None,
        format: Optional[str] = None,
        requestFrom: Optional[str] = None,
):
    """
     The API provides the estimated current position of buses. Currently, it provides the position of ATAF&Linea buses based on the timetable.

     args:
        - agency: str, The agency of interest (optional). The agency can be identified through its URI, or through its name. If not specified, the default agency is used that is configured for the Knowledge Base (e.g. ATAF for Tuscany).
                    Example: Ataf&Linea
        - line: str, The line of interest (optional). The line can be identified through its URI, or through its name. If not specified, positions of all buses are returned.
                    Example: http://www.disit.org/km4city/resource/48-UrbanoAreaMetropolitanaFiorentina-gtfs_Route_2191078216
        - uid: str, Optional user identifier.
                    Example: e7c13b5ce309dcddce9f72c810c3f93c61ac1c47d66126127f7a78bd5c2cb8a2
        - format: str, HTML, or JSON.
                    Available values : html, json
                    Default value : json
        - requestFrom: str, The parameter identifies the request's originator for monitoring purposes.
    required:
        - either 'agency' or 'line'.
    :return:
    """
    url = f"{TPL_BASE_URL}/tpl/bus-position"
    params = {}
    for key, value in {
        "agency": agency,
        "line": line,
        "uid": uid,
        "format": format,
        "requestFrom": requestFrom
    }.items():
        if value:
            params[key] = value

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

# ------------------------ FEEDBACKS ------------------------

# ------------------------ ROUTING ------------------------
@mcp.tool()
async def route_shortest_path(
        source: str,
        destination: str,
        routeType: Optional[str] = None,
        startDateTime: Optional[str] = None,
        format: Optional[str] = None,
        uid: Optional[str] = None,
        requestFrom: Optional[str] = None,
):
    """
    This API allows to get a path from a source point to a destination point. The points can be specified as latitude;longitude coordinates or using the serviceUri of a service. The path is provided as WKT geometry and as a sequence of arcs between nodes (the service uses the OpenStreetMap road graph). The type of route can be specified as using public transport, feet, or car. The start datetime is used to select the options for public_transport and to evaluate the time needed to make the path

    args:
        - source: str, lat;long or service URI of the starting point.
                    Example: 43.7767;11.2477
        - destination: str, lat;long or service URI of the destination.
                    Example: 43.7687;11.2620
        - routeType: str, Can be public_transport, foot_shortest, foot_quiet, or car. It defaults to foot_shortest.
                    Example: foot_shortest
                    Available values : public_transport, foot_shortest, foot_quiet, car
                    Default value : foot_shortest
        - startDateTime: str, Date and time of start. It defaults to the current date and time.
                    Example: 2017-01-13T12:34:00
        - format: str, The output format. It can be json, or html. It defaults to json.
                    Example: html
                    Available values : json, html
                    Default value : json
        - uid: str, A user identifier.
                    Example: e7c13b5ce309dcddce9f72c810c3f93c61ac1c47d66126127f7a78bd5c2cb8a2
        - requestFrom: str, The parameter identifies the request's originator for monitoring purposes
    required:
        - source: str
        - destination: str
    :return:
    """
    url = f"{TPL_BASE_URL}/shortestpath"
    params = {}
    for key, value in {
        "source": source,
        "destination": destination,
        "routeType": routeType,
        "startDateTime": startDateTime,
        "format": format,
        "uid": uid,
        "requestFrom": requestFrom
    }.items():
        if value:
            params[key] = value

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
