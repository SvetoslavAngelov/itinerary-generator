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

async def ChatComplDescription(START: str, COUNTRY: str, MODEL: str = "gpt-4", TEMP: float = 0.5):
    response = await openai.ChatCompletion.acreate(
        model = MODEL, 
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "name": "example_user", "content": "Generate a one day itinerary to visit the top tourist attractions in London, UK."},
            {"role": "system", "name": "example_assistant", "content": "Start your day with the iconic Tower Bridge, not only one of London's most recognizable landmarks, but also a testament to the marvels of Victorian engineering. A short journey via the tube or bus will take you to the British Museum. Immerse yourself in world history with its vast collection of artifacts from all over the globe. Next head over to Covent Garden, known for its vibrant atmosphere, street performers, and eclectic mix of shops and boutiques. Your last stop is the magnificent St. Paul's Cathedral, an architectural masterpiece designed by Sir Christopher Wren.|Tower Bridge|The British Museum|Covent Garden|St. Paul's Cathedral"},
            {"role": "system", "name": "example_user", "content": "Generate a one day itinerary to visit the top tourist attractions in Lyon, FR."},
            {"role": "system", "name": "example_assistant", "content": "Begin your day by making your way up the Fourvière Hill to the stunning Basilique Notre Dame de Fourvière. Next, head to the southern tip of the Presqu'île to visit the Musée des Confluences, an architectural marvel where the Rhône and Saône rivers meet.|Basilique Notre Dame de Fourviere|The Musée des Confluences"},
            {"role": "user", "content": f"Generate a one day itinerary to visit the top tourist attractions in {START}, {COUNTRY}."},
        ],
        temperature = TEMP
    )
    return response["choices"][0]["message"]["content"]