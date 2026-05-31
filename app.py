import json
import streamlit as st

from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage

# Import tools
from tools.flights_filtering_tool import find_best_flights
from tools.hotels_filtering_tool import finding_best_hotels
from tools.weather_lookup_tool import finding_weather_for_required_days
from tools.places_recomendation_tool import finding_best_places
from tools.budget_estimation_tool import itinerary_building


# Streamlit Page
st.set_page_config(
    page_title="Agent AI based travel planning assistant",
    page_icon="✈️"
)

st.title("✈️ AI Travel Planning Assistant")


# User input
query = st.text_area(
    "Enter your travel query",
    placeholder="Example: Plan a 3-day trip from Bangalore to Goa from 2026-05-28 to 2026-05-30"
)


# Generate button
if st.button("Generate Itinerary"):

    if query == "":
        st.warning("Please enter a query.")

    else:

        with st.spinner("Planning your trip..."):

            # Initialize local model
            llm = ChatOllama(
                model="llama3",
                temperature=0.7
            )

            # Prompt
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
            - source
            - destination
            - start_date
            - end_date
            - duration

            User Query:
            {query}
            """

            # LLM response
            response = llm.invoke([
                HumanMessage(content=prompt)
            ])

            cleaned_response = response.content.strip()

            cleaned_response = cleaned_response.replace(
                "```json",
                ""
            )

            cleaned_response = cleaned_response.replace(
                "```",
                ""
            )

            cleaned_response = cleaned_response.strip()


            # Convert JSON
            try:
                trip_details = json.loads(cleaned_response)

            except json.JSONDecodeError:

                st.error("Invalid JSON returned by model")

                st.text(cleaned_response)

                st.stop()


            # Extract values
            source = trip_details["source"]

            destination = trip_details["destination"]

            start_date = trip_details["start_date"]

            end_date = trip_details["end_date"]

            duration = trip_details["duration"]


            # Flight tool
            flight_result = find_best_flights.invoke({

                "source": source,

                "destination": destination
            })


            # Hotel tool
            hotel_result = finding_best_hotels.invoke({

                "city": destination
            })


            # Weather tool
            weather_result = finding_weather_for_required_days.invoke({

                "city": destination,

                "start_date": start_date,

                "end_date": end_date
            })


            # Places tool
            places_result = finding_best_places.invoke({

                "city": destination
            })


            # Final itinerary
            final_result = itinerary_building.invoke({

                "city": destination,

                "duration": duration,

                "flight_info": flight_result,

                "hotel_info": hotel_result,

                "weather_details": weather_result,

                "places": places_result
            })


        # Display ONLY final itinerary
        st.success("Trip Plan Generated Successfully!")

        st.subheader("🗺️ Your Travel Itinerary")

        st.text(final_result)
    with st.sidebar:

        st.header("Why These Recommendations?")

        st.info("""
        Flight selected because it offers
        the best balance between price and duration.
        """)

        st.info("""
        Hotel selected based on affordability
        and customer rating.
        """)

        st.info("""
        Weather forecast analyzed to help
        schedule sightseeing activities.
        """)

        st.info("""
        Tourist places selected from the most
        popular attractions in the destination city.
    """)