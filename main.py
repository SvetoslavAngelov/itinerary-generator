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

    itinerary = list()

    for i in range(len(locations)-1):
        # Obtain the geo code of each location pair
        origin = locations[i]
        origin_geocode = await GeoCodeLocation(access_token, origin, country)
        destination = locations[i+1]
        destination_geocode = await GeoCodeLocation(access_token, destination, country)

        # Calculate ETA between the origin and destination
        distance_km, travel_minutes = await GetEta(access_token, origin_geocode, destination_geocode)
        itinerary.append(f"Travel time between {origin} and {destination} is {distance_km:.2f} kilometers and {travel_minutes:.0f} minutes")

    # Show the final itinerary
    print(locations)
    print("-------------------------------")
    print(itinerary)

    return 

if __name__ == "__main__":
    asyncio.run(main())