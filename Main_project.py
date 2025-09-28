import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from agents import Farmer_Agents
from tasks import Farmer_Tasks
from dotenv import load_dotenv
from crewai import Crew
import edge_tts
import requests
import asyncio
import random
import os
import pygame
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
import json
import pandas as pd
from datetime import datetime
from crewai import LLM


import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
gemini_api_key = os.getenv("GEMINI_API_KEY")
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")

# Configure Gemini
genai.configure(api_key=gemini_api_key)
# model = genai.GenerativeModel('gemini/gemini-2.0-flash')
llm = LLM(
    model="gemini/gemini-1.5-flash",   # ✅ include "gemini/"
    api_key=gemini_api_key
)





VOICE = "en-IN-PrabhatNeural"
OUTPUT_FILE = "response.mp3"

# Text to Speech
async def amain(TEXT):
    communicator = edge_tts.Communicate(TEXT, VOICE)
    await communicator.save(OUTPUT_FILE)

    pygame.mixer.init()
    pygame.mixer.music.load(OUTPUT_FILE)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    os.remove(OUTPUT_FILE)

# Soil Data Generator
def get_soil_data():
    return {
        "moisture": round(random.uniform(15, 35), 2),
        "temperature": round(random.uniform(20, 35), 2),
        "pH": round(random.uniform(5.5, 7.5), 2),
        "nitrogen": round(random.uniform(50, 150), 2),
        "phosphorus": round(random.uniform(30, 90), 2),
        "potassium": round(random.uniform(100, 250), 2),
    }

# Weather Data
def get_weather_data(city: str, api_key: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Weather API Error:", response.text)
    data = response.json()
    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }




# Speech to Text
def listen_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=1)
        st.write("Listening... 🎤")
        audio = recognizer.listen(mic)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."

# File I/O
def save_text_to_file(text, filename="data.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

def load_text_from_file(filename="data.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()
    








# UI
st.set_page_config(page_title="AI Farming Assistant", layout="centered")
st.sidebar.title("🧭 Select Tool")
app = st.sidebar.selectbox("Choose an assistant", ["🌾 Smart Farming Advisor", "🎤 AI Crop Assistant", "💧 Irrigation Advisory"])



bandwidth = ["High", "Medium", "Low"]
selected_crop = st.selectbox("Select the Bandwidth:", bandwidth)

# Save selection to local JSON file
with open("selected_crop.txt", "w") as f:
    f.write(selected_crop)

# # ============== Page 1 ==============
if app == "🌾 Smart Farming Advisor":
    st.title("🌾 Smart Farming Advisor using AI Agents")
    city = st.text_input("Enter your city (for weather data):", "Rawalpindi")

    if st.button("Get Advisory"):
        with st.spinner("Collecting data and analyzing..."):
            soil_data = get_soil_data()
            weather_data = get_weather_data(city, openweather_api_key)

            st.subheader("🔬 Soil Data")
            st.json(soil_data)

            st.subheader("☁️ Weather Data")
            st.json(weather_data)


    ##################################################################################################
                # Agents
    ##################################################################################################
            agents = Farmer_Agents()
            soil_analysis_agent = agents.soil_analysis_agent()
            weather_analysis_agent = agents.weather_analysis_agent()
            crop_selection_agent = agents.crop_selection_agent()

            advisory_agent = agents.advisory_agent()


    ##################################################################################################
    # Tasks
    ##################################################################################################

            tasks = Farmer_Tasks()
            
            Soil_Analysis_Task = tasks.Soil_Analysis_Task(
                agent=soil_analysis_agent, 
                soil_sensor_data=soil_data
                )
            
            Weather_Analysis_Task = tasks.Weather_Analysis_Task(
                agent=weather_analysis_agent, 
                weather_data=weather_data
                )
            
            Crop_Selection_Task = tasks.Crop_Selection_Task(
                agent=crop_selection_agent, 
                soil_analysis_output = Soil_Analysis_Task,
                weather_analysis_output =  Weather_Analysis_Task, 
                context=[Soil_Analysis_Task, Weather_Analysis_Task]
                )
          
            
            Advisory_Message_Task = tasks.Advisory_Message_Task(
                agent=advisory_agent, 
                crop_recommendations = Crop_Selection_Task,  
                context=[Soil_Analysis_Task, Weather_Analysis_Task, Crop_Selection_Task]
                )
            

            crew = Crew(
                agents=[soil_analysis_agent, weather_analysis_agent, crop_selection_agent, advisory_agent],
                tasks=[Soil_Analysis_Task, Weather_Analysis_Task, Crop_Selection_Task ,Advisory_Message_Task],
            )

            results = crew.kickoff()

            st.success("✅ Advisory Generated!")
            st.subheader("📢 Final Advisory")
            ai_response = results.raw
            save_text_to_file(ai_response)
            # st.text(ai_response)
            asyncio.run(amain(ai_response))
            

# # ============== Page 2 ==============
elif app == "🎤 AI Crop Assistant":



        st.title("🎤 AI Crop Assistant")
        # suggestedCrops = ["wheat", "maize", "sunflower"]
        soil_data = get_soil_data()

        if st.button("Start Voice Advisory"):
            while True:
                user_question = listen_speech()

                if user_question.lower() == "exit":
                    st.write("Chat ended. Restart to begin again.")
                    break
                

                answer_passed = load_text_from_file()
                

                agents = Farmer_Agents()
                # urdu_agri_advisor_agent = agents.urdu_agri_advisor_agent()
                crop_comparison_agent = agents.crop_comparison_agent()
                soil_weather_analysis_agent = agents.soil_weather_analysis_agent()
                final_advisory_agent = agents.final_advisory_agent()

                tasks = Farmer_Tasks()
                Crop_Comparison_Task = tasks.Crop_Comparison_Task(
                    agent=crop_comparison_agent,
                    # soil_data=soil_data,
                    suggestedCrops=answer_passed,
                    user_question=user_question
                )
                Soil_Weather_Advisor_Task = tasks.Soil_Weather_Advisor_Task(
                    agent=soil_weather_analysis_agent,
                    soil_data=soil_data,
                    user_question=user_question
                )
                Final_Advisory_Task = tasks.Final_Advisory_Task (
                    agent=final_advisory_agent,
                    comparison_output = Crop_Comparison_Task,
                    soil_weather_output = Soil_Weather_Advisor_Task,
                
                )

                crew = Crew(
                    agents=[crop_comparison_agent, soil_weather_analysis_agent, final_advisory_agent],
                    tasks=[Crop_Comparison_Task, Soil_Weather_Advisor_Task, Final_Advisory_Task],
                )

                results = crew.kickoff()

                ai_response = results.raw
                st.success("✅ Advisory Generated!")
                # st.write(ai_response)
                st.write("AI speaking")
                # st.write(answer_passed)
                asyncio.run(amain(ai_response))

# # ============== Page 3 ==============
elif app == "💧 Irrigation Advisory":

        st.title("💧 Irrigation Decision Support")
        load_dotenv()

        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
        
        def get_farm_details(farm_id, resources_file, env_file, weather_file):
            # --------------------
            # Load files
            # --------------------
            with open(resources_file) as f:
                farm_data = json.load(f)

            with open(env_file) as f:
                env_data = json.load(f)

            weather_df = pd.read_csv(weather_file)

            # normalize farm_data into a list
            farm_list = farm_data if isinstance(farm_data, list) else [farm_data]

            # find main farm
            farm_res = next((f for f in farm_list if f["farm_id"] == farm_id), None)
            if not farm_res:
                return {"error": f"Farm {farm_id} not found"}

            # collect all farms: main + neighbors
            farm_ids = [farm_id] + farm_res.get("neighboring_farms", [])

            results = []

            # --------------------
            # Prepare environment lookup (filter by current date’s day)
            # --------------------
            today_day = datetime.today().day
            env_lookup = {}

            if isinstance(env_data, list):
                for entry in env_data:
                    if "date" in entry:
                        try:
                            entry_day = datetime.strptime(entry["date"], "%Y-%m-%d").day
                        except ValueError:
                            continue  # skip bad date format
                        if entry_day == today_day:  # 👈 only match day
                            env_lookup[entry["farm_id"]] = entry
            elif isinstance(env_data, dict) and "farm_id" in env_data:
                if "date" in env_data:
                    try:
                        entry_day = datetime.strptime(env_data["date"], "%Y-%m-%d").day
                        if entry_day == today_day:
                            env_lookup[env_data["farm_id"]] = env_data
                    except ValueError:
                        pass

            # --------------------
            # Collect details
            # --------------------
            for f_id in farm_ids:
                details = {"farm_id": f_id}

                # resources
                f_res = next((f for f in farm_list if f["farm_id"] == f_id), None)
                if f_res:
                    details["irrigation_hours_per_week"] = f_res["irrigation_hours_per_week"]
                    details["fertilizer_kg_available"] = f_res["fertilizer_kg_available"]
                    details["equipment_availability"] = f_res["equipment_availability"]

                # environment
                if f_id in env_lookup:
                    env = env_lookup[f_id]
                    details.update({
                        "tehsil": env["tehsil"],
                        "district": env["district"],
                        "province": env["province"],
                        "crop_type": env["crop_type"],
                        "soil_moisture_%": env["soil_moisture_%"],
                        "temperature_c": env["temperature_c"],
                        "humidity_%": env["humidity_%"],
                        "pest_detection": env["pest_detection"]
                    })

                    # Weather info (match by tehsil/district/province)
                    match = weather_df[
                        (weather_df["tehsil"] == env["tehsil"]) &
                        (weather_df["district"] == env["district"]) &
                        (weather_df["province"] == env["province"])
                    ]
                    if not match.empty:
                        row = match.iloc[0]
                        details.update({
                            "rainfall_mm": int(row["rainfall_mm"]),
                            "temperature_c_weather": float(row["temperature_c"]),
                            "humidity_%weather": int(row["humidity_%"]),
                            "extreme_event": str(row["extreme_event"])
                        })

                results.append(details)

            return results


        # --------------------
        # Example usage
        # --------------------
        farm_id = "F-001" # 👈 user gives ID
        resources_file = "datasets/farm_resources.json"
        env_file = "datasets/farm_sensor_data_tehsil_with_date.json"
        weather_file = "datasets/weather_data_tehsil.csv"

        result = get_farm_details(farm_id, resources_file, env_file, weather_file)
        print(json.dumps(result, indent=2))

        # Keys you want to exclude temporarily
        exclude_irri_keys = ["irrigation_hours_per_week", "equipment_availability", "fertilizer_kg_available","tehsil", "district", "province","pest_detection",]
        include_harv_keys = ["equipment_availability"]
        include_pest_keys = ["pest_detection"]
        include_rag_keys = ["crop_type"]

        # Make a copy without those keys
        irri_agent = [
        {k: v for k, v in farm.items() if k not in exclude_irri_keys}
        for farm in result
        ]

        harv_agent = [
        {k: v for k, v in farm.items() if k in include_harv_keys}
        for farm in result
        ]

        pest_agent = [
        {k: v for k, v in farm.items() if k in include_pest_keys}
        for farm in result
        ]


        rag_agent = [
        {k: v for k, v in farm.items() if k in include_rag_keys}
        for farm in result
        ]
        # Get current date
        current_date = datetime.now().date()

        st.write(rag_agent)
        if st.button("Get Advisory"):
               





                csv_file_path = "market_prices.csv"  # Replace with your CSV file path
                df = pd.read_csv(csv_file_path)

                # texts = df.apply(lambda row: " | ".join([str(x) for x in row.values]), axis=1).tolist()
                texts = "In Karachi, rice and wheat are in high demand, with rice selling at approximately PKR 150 per kg and wheat at PKR 120 per kg. Cotton and sugarcane also have moderate demand in Karachi, priced around PKR 200 per kg and PKR 90 per kg respectively. In Lahore, wheat and vegetables see the highest consumption, with wheat at PKR 125 per kg and vegetables averaging PKR 60 per kg. Maize and rice also maintain steady sales in Lahore, around PKR 100 and PKR 155 per kg. Multan shows strong demand for sugarcane and cotton, selling at PKR 95 and PKR 210 per kg respectively, while rice and vegetables have moderate sales. Faisalabad primarily demands wheat and vegetables, priced at PKR 122 and PKR 65 per kg, with maize in moderate demand. Peshawar has high consumption of wheat and maize, approximately PKR 118 and PKR 105 per kg, while rice and vegetables sell moderately. Quetta shows steady demand for vegetables and wheat, priced at PKR 70 and PKR 120 per kg, and lower demand for rice, maize, cotton, and sugarcane."
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,
                    chunk_overlap=50
                )
                docs = text_splitter.split_text("\n".join(texts))

                # embeddings = GoogleGenerativeAIEmbeddings(
                #     model="models/text-embedding-004",
                #     api_key='GEMINI_API_KEY'
                # )

                # vectorstore = FAISS.from_texts(docs, embedding=embeddings)
                embeddings = OllamaEmbeddings(model="nomic-embed-text")

                # Create FAISS Vectorstore
                vectorstore = FAISS.from_texts(docs, embedding=embeddings)
                                # Optional: Save FAISS DB locally
                vectorstore.save_local("faiss_db")

                # llm = ChatGoogleGenerativeAI(
                # model="gemini-2.0-flash",
                # api_key='GEMINI_API_KEY'
                #     )
                # ---- LLM (Llama 3.2 from Ollama) ----
                llm = Ollama(
                    model="llama3.2",   # You can also use "llama3.2:70b" if you have it pulled
                    temperature=0
                )


                prompt_template = """
                            Aap ek assistant hain jo farmer data aur market trends ke base par sawalat ka jawab deta hai roman urdu mein. 
                            Use retrieved documents for reference.

                            Question: {question}
                            Context: {context}

                            Answer in short and clear Roman Urdu, specifically mentioning only the crop named in the question:
                            - Us crop ka kaun sa city mein zyada demand hai
                            - Us crop ka wahan selling price kya hai
                            - Baaki kisi crop ki info mat dein
                            """


                prompt = PromptTemplate(template=prompt_template, input_variables=["question","context"])

                # qa_chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=prompt)

                qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=vectorstore.as_retriever(search_kwargs={"k": 10}),
                chain_type="stuff",
                chain_type_kwargs={"prompt": prompt}
                )

                def ask_query(query):
                    result = qa_chain.run(query)
                    return result


                user_query = f"Tell me about {rag_agent}"
                answer = ask_query(user_query)
                # st.write(answer)

                agents = Farmer_Agents()
                irrigation_priority_weather_agent = agents.irrigation_priority_weather_agent()
                harvest_prediction_agent = agents.harvest_prediction_agent()
                pest_advisor_agent = agents.pest_advisor_agent()
                farmer_summary_advisor_agent = agents.farmer_summary_advisor_agent()

                tasks = Farmer_Tasks()
                Irrigation_Priority_Weather_Task = tasks.Irrigation_Priority_Weather_Task(
                    agent=irrigation_priority_weather_agent, 
                    farmers_data=irri_agent,
                    )
                
                Harvest_Prediction_Task_Seasonal = tasks.Harvest_Prediction_Task_Seasonal(
                    agent=harvest_prediction_agent, 
                    farmers_data=harv_agent,
                    current_date=current_date,
                )

                Pest_Advisor_Task = tasks.Pest_Advisor_Task(
                    agent=pest_advisor_agent, 
                    farmers_data=pest_agent,
                )

                Farmer_Summary_Advisor_Task = tasks.Farmer_Summary_Advisor_Task(
                    agent=farmer_summary_advisor_agent,
                    irrigation_output=Irrigation_Priority_Weather_Task,
                    harvest_output=Harvest_Prediction_Task_Seasonal,
                    pest_output=Pest_Advisor_Task,
                    rag_output = answer
                )


                crew = Crew(
                    agents=[irrigation_priority_weather_agent,harvest_prediction_agent,pest_advisor_agent,farmer_summary_advisor_agent],
                    tasks=[Irrigation_Priority_Weather_Task,Harvest_Prediction_Task_Seasonal,Pest_Advisor_Task,Farmer_Summary_Advisor_Task], 
                                )
                
                results = crew.kickoff()
                ai_response = results.raw
                st.write(ai_response)
                st.success("✅ Advisory Generated!")
                st.write(ai_response)
                asyncio.run(amain(ai_response))
