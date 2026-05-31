# For API calls and HTTP requests to access Open-Meteo and receive JSON data 
import requests

# Importing tools from langchain open source platform for building agentic AI applications
# The tools decorator converts python function into Langchain tools which can be directly called by the agents
from langchain.tools import tool


# Helper function for converting weather codes received from the API into descriptions
# The API returns number codes which are converted into weather conditions using this function
def find_weather_condition(code):

    # Dictionary to store weather codes and conditions for Open-Meteo
    climatic_conditions = {
        0: "Sunny",
        1: "Mostly Sunny",
        2: "Partly Cloudy",
        3: "Cloudy",
        45: "Foggy",
        48: "Foggy",
        51: "Light Drizzle",
        61: "Rainy",
        63: "Moderate Rain",
        65: "Heavy Rain",
        71: "Snow",
        80: "Rain Showers",
        95: "Thunderstorm"
    }

    return climatic_conditions.get(
        code,
        "No weather info available"
    )


@tool
def finding_weather_for_required_days( city: str, start_date: str, end_date: str) -> str:

    # Documenting the description which helps LLM to understand the function and analyze when to call it.
    """
    Get weather forecast for the required city
    between the required dates.
    """

    # Step 1: Geocoding API
    # Stores URL for converting city names into coordinates (latitude & longitude)
    geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
    # Exception handling for preventing API crash due to timelag in response from meteo server
    try:

        # API request to get geo coordinates for the required city
        geocode_response = requests.get(
            geocode_url,
            params={"name": city},
            timeout=10 # max waiting time 10 secs
        )

        # Convert JSON data into Python dictionary
        geocode_data_json = geocode_response.json()

    # If response takes too much tme
    except requests.exceptions.Timeout:
        return "Geo-coding response time out. "

    # Handling internet issues
    except requests.exceptions.RequestException:
        return "Unable to connect to geocoding services."

    # Handling Unexpected error
    except Exception:
        return "Geocoding services temporarily unavailable."


    # If city not found
    if "results" not in geocode_data_json:
        return "City not found."


    # Gets latitude value of the first city from the data stored in results list
    latitude = geocode_data_json["results"][0]["latitude"]

    # Gets longitude value of the first city from the data stored in results list
    longitude = geocode_data_json["results"][0]["longitude"]


    # Step 2: Get weather
    # URL to get weather forecast from city coordinates
    weather_info_url = "https://api.open-meteo.com/v1/forecast"

    # Dictionary containing API request settings
    weather_request_parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "auto"  # Automatically uses local timezone of city
    }

    # Exception Handling for API requests
    try:

        # Weather API call
        weather_response = requests.get(
            weather_info_url,
            params=weather_request_parameters,
            timeout=10
        )

        # If API request fails i.e.., statuscode is not equal to 200 (200 is success status code)
        if weather_response.status_code != 200:
            return f"""
Unable to fetch weather data.

Status Code: {weather_response.status_code}
"""

        # Convert JSON into Python dictionary
        weather_data = weather_response.json()
    # If response takes too much tme
    except requests.exceptions.Timeout:
        return "Weather response time out."
    # Handling internet issues
    except requests.exceptions.RequestException:
        return "Unable to connect to weather services."
    # Handling Unexpected error
    except Exception:
        return "Weather service temporarily unavailable."


    # Print weather data for debugging
    print(weather_data)


    # If daily weather data unavailable
    if "daily" not in weather_data:
        return f"Weather data unavailable: {weather_data}"


    # Storing daily weather data
    daily_weather_data = weather_data["daily"]


    # Step 3: Build response
    result = f"""
Weather forecast for {city} from {start_date} to {end_date}:

"""


    # For all required days
    # (daily_weather_data["time"] contains date list
    # eg: ["2026-05-20", "2026-05-21"])
    for i in range(len(daily_weather_data["time"])):

        # Calling helper function to get weather description
        weather_condition = find_weather_condition(
            daily_weather_data["weather_code"][i]
        )

        result += f"""
Day: {daily_weather_data['time'][i]}
Weather: {weather_condition}
Max Temp: {daily_weather_data['temperature_2m_max'][i]}°C
Min Temp: {daily_weather_data['temperature_2m_min'][i]}°C

"""

    return result