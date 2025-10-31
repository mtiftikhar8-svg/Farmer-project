
# 🌾 AI-Powered Agricultural Assistant using Agentic AI

## 📘 Title
AI-Powered Agricultural Assistant for Crop and Irrigation Advisory using Agentic AI

---

## 🧠 Description
This project presents an intelligent, voice-to-voice multi-agent agricultural advisory system designed to assist farmers in making better crop selection and irrigation (watering) decisions.
Unlike traditional text-based systems, this application interacts entirely through speech, making it highly accessible for farmers who may not be able to read or write.
The system listens to the farmer’s voice query, analyzes real-time soil and weather conditions, recommends the most suitable crops, compares the farmer’s selected crop with system suggestions, and provides final irrigation guidance — advising whether watering is needed and when to irrigate next.
All advisories are delivered in Roman Urdu through voice output, ensuring clarity, convenience, and usability for uneducated or semi-literate users.

The solution leverages the **CrewAI framework** for agentic collaboration and **Google Gemini 2.0 Flash Exp** as the core reasoning model, integrating **OpenWeather API** for real-time environmental data.

---

## 🌱 Dataset Information
The system uses **self-generated (synthetic) soil data** and **real-time weather data**:

- **Soil Data:** Generated internally by `get_soil_data()` function  
  - Parameters: Moisture, pH, Nitrogen, Phosphorus, Potassium, Temperature  
- **Weather Data:** Retrieved from OpenWeather API via `get_weather_data(city, api_key)`  
  - Parameters: Temperature, Humidity, Wind Speed, Weather Description  

A sample of generated data is saved as **`self_curated_dataset.csv`** for reviewers.

---

## 💻 Code Information
The project is modular and based on **CrewAI** agents:
1. **Soil & Weather Analysis Agent** – interprets soil and weather parameters.  
2. **Crop Recommendation Agent** – suggests top three suitable crops.  
3. **Crop Comparison Agent** – compares farmer’s choice with AI suggestions.  
4. **Final Advisory Agent** – delivers a polite, concise response in Roman Urdu.  

The main logic, dataset generation, and agent coordination are implemented in **`main.py`**.

---

## ⚙️ Usage Instructions

### Step 1 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Add Your API Key
Insert your OpenWeather and GEMINI API key into the script (or `.env` file):
```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
```

### Step 3 — Run the Application
```bash
streamlit run main.py
```

### Step 4 — Interact with the Interface
Module 1 — Crop Recommendations:
Simply click on “Get Advisory”. The system will automatically analyze soil and weather conditions and provide the top 3 recommended crops for your area.

Module 2 — Crop Comparison:
If you already have a crop in mind, move to this module.
Speak your crop name and mention that you plan to grow it — the AI agent will compare your selected crop with the recommended ones and inform you whether it is suitable or not based on soil and weather data.

Module 3 — Irrigation Advisory:
If you have already planted a crop, go to this module.
Speak your city name and crop name, and the AI system will respond in Roman Urdu, informing you whether your crop needs watering at this time or not, along with additional irrigation advice.

---

## 🧩 Requirements
- **Python:** ≥ 3.9  
- **Frameworks/Libraries:**
  - CrewAI  
  - Google Gemini 2.0 Flash Exp (via API)  
  - Streamlit  
  - Requests  
  - Python-dotenv  

---

## 🧮 Methodology
1. Collect or simulate soil and weather data.  
2. Analyze environmental parameters using AI agents.  
3. Recommend optimal crops based on soil–weather suitability.  
4. Compare farmer input with AI suggestions.  
5. Generate a natural-language advisory in Roman Urdu explaining crop suitability and irrigation timing.  

---

## 📚 Citations
This work is part of an academic research project titled:  
**“AI-Powered Agricultural Advisory System using Agentic AI for Crop and Irrigation Decision Making”**  
and references:
- Google Gemini 2.0 Flash Exp Model (2024)  
- CrewAI Framework Documentation (2024)  
- OpenWeather API Documentation (2024)

---

## 📄 License & Contribution
This project is intended for **academic and research purposes only**.  
External contributions are welcome through pull requests for educational improvements.  
Commercial use is not permitted without prior consent.
