''' Importing json module for reading the json data file, read it and convert the data into python objects
 Such as a json format into a list of dictionaries which can be easily processed'''
import json
# Importing tools from langchain open source platform for building agentic AI applications
# The tools decorator converts python function into Langchain tools which can be directly called by the agents
from langchain.tools import tool
# For reading data files
import os

current_directory = os.path.dirname(__file__)

json_path_forhotelsdata = os.path.join(current_directory, "..", "data", "hotels.json")

@tool
def finding_best_hotels(city: str) -> str:
    # Documenting the description which helps LLM to understand the function and analyze when to call it.
    """
    Find best hotels in the city.
    """
    # Loading JSON data for hotels
    with open(json_path_forhotelsdata, "r") as hotels_data_file:
        # converting json data into python data
        hotels_data = json.load(hotels_data_file)

    # Filtering available hotels by required city
    available_hotels = [
        hotel for hotel in hotels_data
        if hotel["city"].lower() == city.lower()
    ]

    # If no hotels available
    if len(available_hotels)==0:
        return "No hotels available."
    
    # Highest rated hotel available
    top_rated_hotel = [
        hotel
        for hotel in available_hotels
        if hotel["stars"] >= 4
    ]

    # Cheapest  top rated hotel available
    cheapest__top_rated_hotel = min(top_rated_hotel, key=lambda x: x["price_per_night"])

    # Create multiline response
    result = f"""
Hotel booked at {cheapest__top_rated_hotel['city']}: 
Hotel: {cheapest__top_rated_hotel['name']}
Price per night: ₹{cheapest__top_rated_hotel['price_per_night']}
Rating: {cheapest__top_rated_hotel['stars']} star
"""

    return result