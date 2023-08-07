import openai

async def ChatComplDefault(START: str, COUNTRY: str, MODEL: str = "gpt-4", TEMP: float = 0.5):
    response = await openai.ChatCompletion.acreate(
        model = MODEL, 
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "name": "example_user", "content": "Generate a one day itinerary to visit the top tourist attractions in London, UK."},
            {"role": "system", "name": "example_assistant", "content": "Tower Bridge|The British Museum|Covent Garden|St. Paul's Cathedral"},
            {"role": "system", "name": "example_user", "content": "Generate a one day itinerary to visit the top tourist attractions in San Francisco, US."},
            {"role": "system", "name": "example_assistant", "content": "Golden Gate Bridge|Golden Gate Park|Fisherman's Wharf|Lombard Street"},
            {"role": "system", "name": "example_user", "content": "Generate a one day itinerary to visit the top tourist attractions in Lyon, FR."},
            {"role": "system", "name": "example_assistant", "content": "Basilique Notre Dame de Fourviere|The Musée des Confluences"},
            {"role": "user", "content": f"Generate a one day itinerary to visit the top tourist attractions in {START}, {COUNTRY}."},
        ],
        temperature = TEMP
    )
    return response["choices"][0]["message"]["content"]