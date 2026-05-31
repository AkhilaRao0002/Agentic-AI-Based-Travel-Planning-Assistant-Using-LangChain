''' Importing json module for reading the json data file, read it and convert the data into python objects
 Such as a json format into a list of dictionaries which can be easily processed'''
import json

# Imports the Ollama chat chat model from langchain
from langchain_community.chat_models import ChatOllama
# Importing HumanMessage for sending prompts to LLM 
from langchain.schema import HumanMessage

# Import tools
from tools.flights_filtering_tool import find_best_flights
from tools.hotels_filtering_tool import finding_best_hotels
from tools.weather_lookup_tool import finding_weather_for_required_days
from tools.places_recomendation_tool import finding_best_places
from tools.budget_estimation_tool import itinerary_building


# Step 1 — Initialize Local LLM 
# Using locally installed llama model through Ollama
llm = ChatOllama(
    model="llama3",
    temperature=0.7 # to control randomness ( lower value = more accurate )
)


# Step 2 — Take User Input
input_query = input("Enter your travel query: ")


# Step 3 — Multiline Prompt for extracting trip details
prompt = f"""
Extract travel details from the query.

Return ONLY valid JSON.

Rules:
- No markdown
- No explanations
- No extra text
- JSON must start with {{
- JSON must end with }}
- duration must be integer only

Fields:
- source (string)
- destination (string)
- start_date (YYYY-MM-DD)
- end_date (YYYY-MM-DD)
- duration (integer)

User Query:
{input_query}
"""


# Step 4 — Sending prompt to LLM
response_data = llm.invoke([
    HumanMessage(content=prompt) # wraps prompt into user message
])


# Step 5 — Printing raw response
''' Eg: {
  "source": "Bangalore",
  "destination": "Goa",
  "start_date": "2026-05-28",
  "end_date": "2026-05-30",
  "duration": 3
}'''
print("\nRaw LLM Response:\n")
print(response_data.content)


# Step 6 — Clean response
# Removes extra spaces and lines
cleaned_response_data = response_data.content.strip()

# Removes markdown code blocks
cleaned_response_data = cleaned_response_data.replace(
    "```json",
    ""
)

cleaned_response_data = cleaned_response_data.replace(
    "```",
    ""
)

# Final cleaning
cleaned_response_data = cleaned_response_data.strip()


# Step 7 — Convert JSON string into Python dictionary
# exception handling
try:
    trip_plan_details = json.loads(cleaned_response_data)

except json.JSONDecodeError:

    print("\nInvalid JSON data returned by model.")
    print("\nReturned Response:\n")
    print(cleaned_response_data)

    exit()


# Step 8 — Print extracted details
print("\nExtracted Trip Details:\n")
print(trip_plan_details) #prints parsed dictionary


# Step 9 — Stores extracted variables
source = trip_plan_details["source"]

destination = trip_plan_details["destination"]

start_date = trip_plan_details["start_date"]

end_date = trip_plan_details["end_date"]

duration = trip_plan_details["duration"]


# STEP 10 — Call Flight Tool
print("\nFinding Flights...\n")

flight_result = find_best_flights.invoke({

    "source": source,

    "destination": destination
})

print(flight_result)


# STEP 11 — Call Hotel Tool
print("\nFinding Hotels...\n")

hotel_result = finding_best_hotels.invoke({

    "city": destination
})

print(hotel_result)


# STEP 12 — Call Weather Tool
print("\nGetting Weather Forecast...\n")

weather_result = finding_weather_for_required_days.invoke({

    "city": destination,

    "start_date": start_date,

    "end_date": end_date
})

print(weather_result)


# STEP 13 — Call Places Tool
print("\nFinding Tourist Places...\n")

places_result = finding_best_places.invoke({

    "city": destination
})

print(places_result)


# STEP 14 — Build Final Itinerary
print("\nGenerating Final Itinerary...\n")

final_result = itinerary_building.invoke({

    "city": destination,

    "duration": duration,

    "flight_info": flight_result,

    "hotel_info": hotel_result,

    "weather_details": weather_result,

    "places": places_result
})


# STEP 15 — Final Output
print("\n================ FINAL TRAVEL PLAN ================\n")

print(final_result)