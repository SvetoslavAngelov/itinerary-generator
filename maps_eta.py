import aiohttp
from urllib.parse import quote

# Exchange Maps JS Authorisation token for a Maps Server API Access Token 
async def GetAccessToken(maps_jwt: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+maps_jwt
    }

    async with aiohttp.ClientSession() as session: 
        async with session.get("https://maps-api.apple.com/v1/token", headers=headers) as response: 
            data = await response.json()
            return data["accessToken"]

# Obtain the latitude and longitude for a given address and country in ISO ALPHA-2 code
async def GeoCodeLocation(access_token: str, address: str, country: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+access_token
    }
        
    # Build URL
    base_url = "https://maps-api.apple.com/v1/geocode"
    url = f"{base_url}?q={quote(address)}&limitToCountries={quote(country)}"

    # Create a new session and call the Apple Maps GeoCode endpoint
    async with aiohttp.ClientSession() as session: 
        async with session.get(url, headers=headers) as response: 
            data = await response.json()

    # Extract coordinates 
    coordinates = "0.0,0.0"

    if data["results"][0]["coordinate"]:
        latitude = data["results"][0]["coordinate"]["latitude"]
        longitude = data["results"][0]["coordinate"]["longitude"]

        # Format into a string
        coordinates = f"{latitude},{longitude}"

    return coordinates

# Get distance estimate using Maps Server API's etas endpoint 
async def GetEta(access_token: str, origin_coordinate: str, destination_coordinate: str): 
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+access_token
    }

    # Build URL 
    base_url = "https://maps-api.apple.com/v1/etas"
    url = f"{base_url}?origin={origin_coordinate}&destinations={destination_coordinate}&transportType=Automobile"

    # Create a new session and call the Apple Maps ETAs endpoint 
    async with aiohttp.ClientSession() as session: 
        async with session.get(url, headers=headers) as response: 
            data = await response.json()
    
    # Gather ETA 
    distance_meters = 0
    travel_seconds = 0

    if data["etas"][0]:
        distance_meters = data["etas"][0]["distanceMeters"]
        travel_seconds = data["etas"][0]["expectedTravelTimeSeconds"]

    return distance_meters, travel_seconds
