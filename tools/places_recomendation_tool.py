''' Importing json module for reading the json data file, read it and convert the data into python objects
 Such as a json format into a list of dictionaries which can be easily processed'''
import json
# Importing tools from langchain open source platform for building agentic AI applications
# The tools decorator converts python function into Langchain tools which can be directly called by the agents
from langchain.tools import tool
# For reading data files
import os

current_directory = os.path.dirname(__file__)

json_path_forplacesdata = os.path.join(current_directory, "..", "data", "places.json")

@tool
def finding_best_places(city: str) -> str:
    # Documenting the description which helps LLM to understand the function and analyze when to call it.
    """
    Discovering best places to visit in the city.
    """
    # Loading JSON data for places
    with open(json_path_forplacesdata, "r") as places_data_file:
        # converting json data into python data
        places_data = json.load(places_data_file)

    # Filtering places for exploring in the required city
    available_places = [
        place for place in places_data
        if place["city"].lower() == city.lower()
    ]

    # If no hotels available
    if len(available_places)==0:
        return "No sites to explore available."
    
    # Top sites to explore
    top_rated_places = [
        place
        for place in available_places
        if place["rating"] >= 4
    ]

    # Create multiline response
    # Using loop for recommending places
    sites_details = ""

    for place in top_rated_places:

        sites_details += f"""
Place name : {place['name']}:
Type : {place['type']}
Rating : {place['rating']}

"""
    result = f"""
Places to explore:

{sites_details}
"""
    return result