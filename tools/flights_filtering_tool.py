''' Importing json module for reading the json data file, read it and convert the data into python objects
 Such as a json format into a list of dictionaries which can be easily processed'''
import json
# Importing tools from langchain open source platform for building agentic AI applications
# The tools decorator converts python function into Langchain tools which can be directly called by the agents
from langchain.tools import tool
# For reading data files
import os

current_directory = os.path.dirname(__file__)

json_path_forflightsdata = os.path.join(current_directory, "..", "data", "flights.json")

# For converting date and time into datetime format in python
from datetime import datetime
# Calculating duration by subtracting arrival time by departure time
def get_duration(flight):
    # converting departure and arrival time from ISO string format to datetime format
    departure = datetime.fromisoformat(flight["departure_time"])
    arrival = datetime.fromisoformat(flight["arrival_time"])
    duration = (arrival - departure).total_seconds()/3600
    return duration

# Function for finding cheapest and fastest flights for the given source and destination.
# Passing the parameters source and destination required.
# defining retun type as string using arrow function
# using tool decorator to acces the function as the Langchain tool
@tool
def find_best_flights(source: str, destination: str) -> str:
    # Documenting the description which helps LLM to understand the function and analyze when to call it.
    """
    Find cheapest and fastest flights between source and destination.
    """
    
    # Loading JSON data for flights
    with open(json_path_forflightsdata, "r") as flights_data_file:
        # converting json data into python data
        flights_data = json.load(flights_data_file)

    # Filtering available flights
    available_flights = [
        flight for flight in flights_data
        if flight["from"].lower() == source.lower()
        and flight["to"].lower() == destination.lower()
    ]

    # If no flights available
    if len(available_flights)==0:
        return "No flights available for this route at this time."

    # Find minimum duration
    minimum_duration = min(
    get_duration(flight)
    for flight in available_flights
    )

    # Find all flights with same minimum duration
    fastest_flights = [
        flight
        for flight in available_flights
        if get_duration(flight) == minimum_duration
    ]

    # Cheapest flight available
    cheapest_flight_among_all_fastest_flights = min(fastest_flights, key=lambda x: x["price"])

    # Create multiline response
    result = f"""
Selected Flight from {cheapest_flight_among_all_fastest_flights['from']} to {cheapest_flight_among_all_fastest_flights['to']}:
Flight: {cheapest_flight_among_all_fastest_flights['airline']}
Price: ₹{cheapest_flight_among_all_fastest_flights['price']}
Duration: {get_duration(cheapest_flight_among_all_fastest_flights)} hours
Departure time: leaves {cheapest_flight_among_all_fastest_flights['from']} at {datetime.fromisoformat(cheapest_flight_among_all_fastest_flights["departure_time"]).time()}
"""

    return result

