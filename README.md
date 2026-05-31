# Agentic AI-Based Travel Planning Assistant

## Overview

The Agentic AI-Based Travel Planning Assistant is an intelligent travel planning system that automates itinerary generation using Large Language Models (LLMs), LangChain tools, external APIs, and a Streamlit-based user interface.

The system accepts natural language travel queries from users, extracts trip details, recommends flights, hotels, weather-based travel insights, tourist attractions, estimates travel budgets, and generates personalized day-wise itineraries.

The project uses a locally hosted Llama 3 model through Ollama, enabling private and cost-effective AI-powered travel planning.

---

## Features

* Natural language travel query processing
* Automatic extraction of travel details
* Flight recommendations
* Hotel recommendations
* Weather forecasting using Open-Meteo API
* Tourist attraction recommendations
* Budget estimation
* Day-wise itinerary generation
* Streamlit-based web interface
* Local LLM execution using Ollama and Llama 3

---

## System Architecture

User Query

↓

Streamlit Interface

↓

Llama 3 (Ollama)

↓

LangChain Agent

↓

Flight Tool

Hotel Tool

Weather Tool

Places Tool

↓

Itinerary Builder

↓

Final Travel Plan

---

## Technologies Used

* Python
* LangChain
* Ollama
* Llama 3
* Streamlit
* Open-Meteo API
* Requests
* JSON
* Regular Expressions (Regex)

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/Agentic-AI-Travel-Planning-Assistant.git

cd Agentic-AI-Travel-Planning-Assistant
```

### Create Virtual Environment

```bash
python -m venv travel_env
```

### Activate Virtual Environment

Windows

```bash
travel_env\Scripts\activate
```

Linux/Mac

```bash
source travel_env/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Ollama Setup

### Verify Ollama Installation

```bash
ollama --version
```

### Download Llama 3 Model

```bash
ollama pull llama3
```

### Start Ollama Server

```bash
ollama serve
```

The Ollama server runs locally at:

```text
http://localhost:11434
```

---

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

---

## Example Query

```text
Plan a 3-day trip from Bangalore to Goa from 2026-05-28 to 2026-05-30
```

---

## Example Output

The generated itinerary includes:

* Flight recommendation
* Hotel recommendation
* Weather forecast
* Tourist attractions
* Day-wise travel plan
* Estimated travel budget

Example:

```text
3-Day Trip to Goa

Flight:
IndiGo - ₹4500

Hotel:
Sea View Resort - ₹2500/night

Weather:
Day 1: Sunny
Day 2: Cloudy
Day 3: Sunny

Itinerary:
Day 1: Beach, Fort
Day 2: Museum, Church
Day 3: Market, Lake

Estimated Budget:
Flight: ₹4500
Hotel: ₹7500
Food & Travel: ₹2400

Total Cost: ₹14400
```

---

## Project Structure

```text
project/
│
├── app.py
├── agent.py
│
├── datasets/
│   ├── flights.json
│   ├── hotels.json
│   └── places.json
│
├── tools/
│   ├── flights_filtering_tool.py
│   ├── hotels_filtering_tool.py
│   ├── weather_lookup_tool.py
│   ├── places_recomendation_tool.py
│   └── budget_estimation_tool.py
│
├── requirements.txt
└── README.md
```

---

## Workflow

1. User enters a travel query.
2. Llama 3 extracts structured travel information.
3. Flight recommendation tool selects suitable flights.
4. Hotel recommendation tool identifies accommodations.
5. Weather tool retrieves forecasts using Open-Meteo API.
6. Places recommendation tool suggests tourist attractions.
7. Itinerary builder combines all outputs.
8. Budget estimation is calculated.
9. Final itinerary is displayed through Streamlit.

---

## Business Impact

This project demonstrates how Agentic AI can support modern travel services by:

* Reducing customer support workload
* Providing personalized recommendations
* Automating itinerary generation
* Improving customer satisfaction
* Saving users time and money

The solution aligns with industry trends where travel platforms increasingly adopt conversational and agentic AI technologies.

---

## Future Enhancements

* Real-time flight booking integration
* Real-time hotel booking integration
* User preference learning
* Weather-aware itinerary optimization
* Interactive maps integration
* Multilingual support
* Dynamic pricing analysis
* AI-powered travel assistant chatbot

---

## Author

**Akhila Rao**
