''' Importing json module for reading the json data file, read it and convert the data into python objects
 Such as a json format into a list of dictionaries which can be easily processed '''
import json
# Importing tools from langchain open source platform for building agentic AI applications
# The tools decorator converts python function into Langchain tools which can be directly called by the agents
# Importing tool decorator from LangChain
from langchain.tools import tool

# Importing regular expression module for extracting prices using patterns
import re


@tool
def itinerary_building(city: str, duration: int, flight_info: str, hotel_info: str, weather_details: str, places: str) -> str:
    """
    Builds a complete travel itinerary using
    flight, hotel, weather and places information.
    Also estimates total travel budget.
    """

    # Step 1: Extract place names from places tool output
    # Empty list for storing extracted place names from places tool for the required city 
    places_lines = []

    # splitting and looping through everyilne in places
    for each_line in places.splitlines():

        if "Place name" in each_line:

            # Extracting only place name
            place_name = each_line.split(":")[1].strip()

            places_lines.append(place_name)


    # Step 2: Extract weather information
    weather_lines = []
    # for counting number of days
    current_day = 1
    # Splitting weather string into lines.
    weather_data_lines = weather_details.splitlines()

    for i in range(len(weather_data_lines)):

        if "Weather:" in weather_data_lines[i]:

            weather_condition = weather_data_lines[i].split(":")[1].strip()

            # Getting max temperature
            max_temp = weather_data_lines[i + 1].split(":")[1].strip()

            weather_lines.append(
                f"- Day {current_day}: {weather_condition} ({max_temp})"
            )

            current_day += 1


    # STEP 3: Create itinerary day-wise

    itinerary_result = ""

    total_places = len(places_lines)

    # Base number of places per day
    base_places = total_places // duration

    # Remaining extra places
    extra_places = total_places % duration

    place_index = 0

    for day in range(duration):

        day_places = []

        # First few days get one extra place
        places_today = base_places

        if day < extra_places:
            places_today += 1

        for _ in range(places_today):

            if place_index < total_places:

                day_places.append(
                    places_lines[place_index]
                )

                place_index += 1

        itinerary_result += f"""
    Day {day + 1}: {", ".join(day_places)}
    """

    
    # Step 4: Extract flight price
    flight_price_match = re.search(r"₹(\d+)", flight_info)

    if flight_price_match:

        flight_price = int(flight_price_match.group(1))

    else:

        flight_price = 0


    # Step 5: Extract hotel price per night
    hotel_price_match = re.search(r"₹(\d+)", hotel_info)

    if hotel_price_match:

        hotel_price_per_night = int(hotel_price_match.group(1))

    else:

        hotel_price_per_night = 0


    # Step 6: Calculate hotel total
    hotel_total = hotel_price_per_night * duration


    # Step 7: Estimate food and local travel
    food_and_travel = duration * 800


    # Step 8: Calculate total cost
    total_cost = (
        flight_price
        + hotel_total
        + food_and_travel
    )


    # Step 9: Create final response
    result = f"""
Your {duration}-Day Trip to {city}

Flight Selected:
{flight_info}

Hotel Booked:
{hotel_info}

Weather:
{"".join(weather_lines)}

Itinerary:
{itinerary_result}

Estimated Total Budget:
- Flight: ₹{flight_price}
- Hotel: ₹{hotel_total}
- Food & Travel: ₹{food_and_travel}

-------------------------------------

Total Cost: ₹{total_cost}
"""

    return result