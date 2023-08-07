import os
import asyncio
import argparse
import openai

from maps_eta import GetAccessToken, GeoCodeLocation, GetEta
from chat_cmpl import ChatComplDefault

async def main():

    parser = argparse.ArgumentParser(description="Generate a travel itinerary.")
    parser.add_argument("--start", required=True, help="Type in your start location.")
    parser.add_argument("--country", required=True, help="Specify the country as an ISO ALPHA-2 code.")
    args = parser.parse_args()

    start_location = args.start
    country = args.country

    # Apple Maps JS token
    maps_jwt = os.getenv("MAPS_JWT")

    # OpenAI account details
    openai.organization = os.getenv("OPENAI_ORG")
    openai.api_key = os.getenv("OPENAI_KEY")

    # Get a summary of the trip and a list of locations to visit
    response = await ChatComplDefault(start_location, country)
    locations = response.split("|")

    # Obtain a temporary Apple Maps API access token
    access_token = await GetAccessToken(maps_jwt)

    # Obtain the geocoordinates of each location
    tasks_geocode = [GeoCodeLocation(access_token, location, country) for location in locations]
    location_geocodes = await asyncio.gather(*tasks_geocode)

    # Estimate the distance and ETA between each location 
    origins = list()
    destinations = list()

    for i in range(len(location_geocodes) - 1): 
        if len(location_geocodes[i]) != 0 and len(location_geocodes[i+1]) != 0:
            origins.append(location_geocodes[i])
            destinations.append(location_geocodes[i+1])

    if len(origins) != 0 and len(destinations) !=0:
        tasks_eta = [GetEta(access_token, origin, destination) for origin, destination in zip(origins,destinations)]
        itinerary = await asyncio.gather(*tasks_eta)
    else: 
        itinerary = "Couldn't calculate travel times, try again later!"

    # Show the final itinerary
    print(locations)
    print("-------------------------------")
    print(itinerary)

    return 

if __name__ == "__main__":
    asyncio.run(main())