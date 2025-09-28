from crewai import  Task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os 
from crewai_tools import TavilySearchTool




load_dotenv()

os.environ["TAVILY_API_KEY"] = "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"
os.getenv("GEMINI_API_KEY")

research_tool = SerperDevTool()
# Initialize the Tavily search tool
tavily_tool = TavilySearchTool()

class Farmer_Tasks:

##############################################################################################################
        # Task 1        page 1
##############################################################################################################
    def Soil_Analysis_Task(self, agent, soil_sensor_data):
        return Task(
            description=f"""Analyze the provided soil sensor data for the given agricultural location.

            The agent will:
            - Interpret sensor readings for moisture, temperature, pH, nitrogen, phosphorus, and potassium.
            - Classify the soil type (e.g., loamy, sandy, clayey).
            - Assess the fertility level (low, medium, high) based on nutrient values.
            - Determine which general crop categories (e.g., leafy vegetables, grains, root crops) are suitable for this soil.

            Parameters:
            - Soil Sensor Data: {soil_sensor_data}
        

            The agent will output an analysis of soil quality, structure, and suitability for growing crops.
            """,

            tools=[],
            agent=agent,
            expected_output="""
                    A structured JSON report containing:
                    - Soil Type (e.g., Loamy, Sandy)
                    - Fertility Level (Low, Medium, High)
                    - Suggested Crop Categories (e.g., Leafy Greens, Root Vegetables, Grains)
                 """
        )


##############################################################################################################
        # Task 2        page 1
##############################################################################################################
    def Weather_Analysis_Task(self, agent, weather_data):
        return Task(
            description=f"""Analyze the current weather conditions to assess their suitability for agricultural activity.

            The agent will:
            - Interpret real-time weather data including temperature, humidity, wind speed, and weather description.
            - Determine the climate type (e.g., warm-dry, humid, moderate).
            - Identify any environmental risks to crop growth such as heat stress, low humidity, or high winds.
            - Evaluate the overall growing condition (Favorable, Moderate, or Poor) based on the weather.

            Parameters:
            - Weather Data: {weather_data}
    

            The agent will provide an environmental assessment useful for crop planning.
            """,
            tools=[],
            agent=agent,
            expected_output="""
                    A structured JSON report containing:
                    - Climate Type (e.g., Warm-Dry, Humid-Tropical)
                    - Weather Risks (list of potential risks)
                    - Growing Condition Assessment (Favorable, Moderate, Poor)
                """
        )



##############################################################################################################
        # Task 3        page 1
##############################################################################################################
    def Crop_Selection_Task(self, agent, soil_analysis_output, weather_analysis_output, context):
        return Task(
            description=f"""Using the analyzed soil and weather data, recommend the top 3 crops suitable for cultivation.

            The agent will:
            - Review soil analysis including type, fertility level, and crop category suggestions.
            - Review weather analysis including climate type, risks, and growing conditions.
            - Select the 3 most compatible crops based on combined soil and weather profiles.
            - For each crop, estimate:
                1. Time to harvest (in days)
                2. Watering schedule in human-readable format:
                - If a crop needs watering once a week, write 'once per week'
                - If twice per week, write 'twice per week'
                - If every 2 days, write 'every 2 days'
                - If daily, write 'daily'

            Parameters:
            - Soil Analysis Output: {soil_analysis_output}
            - Weather Analysis Output: {weather_analysis_output}

            The agent will return crop names, growth durations, and watering schedules in clear terms.
            """,
            context=context,
            tools=[],
            agent=agent,
            expected_output="""
                A structured JSON list of 3 crops, each with:
                - Crop Name
                - Estimated Days to Harvest
                - Recommended Watering Schedule (human-readable)
            """
        )





##############################################################################################################
    # Task 4       page 1
##############################################################################################################
    def Advisory_Message_Task(self, agent, crop_recommendations, context, language="Roman Urdu"):
        return Task(
            description=f"""Convert crop recommendations into a clear and friendly advisory message in {language} 
                    for local farmers.

                    The agent will:
                    - Use spoken-style Roman Urdu
                    - Write human-like natural output:
                        - Pehle crop ka naam
                        - Kitne din mein tayar ho gi
                        - Roz kitni dafa pani dena hai
                        - Har dafa pani dene ka time (jaise subha 7 baje, shaam 6 baje)

                    - Message aisa ho jaise koi tajurba kaar kisaan dosray kisaan ko mashwara de raha ho, asaan aur garam lehja mein.

                    Important:
                    - Expected output mein koi symbols na ho jaise dot, bullet, ya colon.
                    - Sirf plain text ho, jaise aam baat cheet mein hota hai.
                    - 'ga' or 'gi' in dono lafzo ka use bhi nhi krna.

                    Parameters:
                    - Crop Recommendations: {crop_recommendations}
                    - Language: {language}

                    Output:
                    Plain Roman Urdu message for farmers based on soil and weather analysis.
                    """,
            context=context,
            tools=[],
            agent=agent,
            expected_output="""
                    G to kisan Bhai main ne aap ki zameen aur mausam ka jaiza lia hai. Mere hisab sy sab se behtareen fasal jo aap laga saktay hain wo hai bhindi. Ye fasal takreeban 60 din mein tayar ho jaye gi aur aap esay market mein achi qeemat par bech saktay hain. Bhindi ko rozana do martaba pani ki zarurat hoti hai pehla pani subha fajar ke baad ya nashtay se pehle dein aur doosra pani shaam mein maghrib ke baad ya raat ke khanay se thodi der pehle dein

                    Dusri behtareen fasal aap ke ilaqay ke liye tamatar hai. Ye lagbhag 75 din mein ready ho jati hai. Esay bhi roz do dafa pani chahiye subha 7 baje ke kareeb aur shaam 6 baje ke aas paas

                    Teesri fasal jo aap ke liye faydamand ho sakti hai wo hai paalak. Paalak 45 din mein ready ho jati hai. Esay sirf ek martaba pani dena kaafi ho ga subha 8 baje ke kareeb pani dein

                    In teenon mein se aap kisi bhi fasal ka intekhab kar saktay hain lekin agar aap jaldi munafa chahte hain to paalak ya bhindi behtareen hainrec. InshaAllah achi paidawaar aur faida hoga
                    """
        )




##################################################################################################
# Task 5       page 2
##################################################################################################
    def Crop_Comparison_Task(self, agent, suggestedCrops, user_question):
        return Task(
            description=f"""
                Compare the user-requested crop with already suggested crops and determine if it is more suitable.

                Parameters:
                - Suggested Crops: {suggestedCrops}
                - User Crop: {user_question}

                The agent will:
                1. Evaluate advantages/disadvantages of the user crop vs suggested crops
                2. State clearly if it is better, worse, or similar
                3. Provide reasoning in concise Urdu (or Roman Urdu)
            """,
            tools=[],
            agent=agent,
            expected_output="""
                A short, clear comparison:
                - If user crop is better: explain why
                - If user crop is worse: explain why
                - If similar: briefly mention similarity
            """
        )


##################################################################################################
# Task 6       page 2
##################################################################################################
    def Soil_Weather_Advisor_Task(self, agent, soil_data, user_question):
        return Task(
            description=f"""
                Determine if the requested crop can be grown according to the provided soil and weather data.

                Parameters:
                - Soil Data: {soil_data}
                
                - Crop: {user_question}

                The agent will:
                1. Check soil parameters (moisture, pH, nutrients) for crop suitability
                2. Recommend YES/NO if the crop can grow
                3. Suggest alternatives if not suitable
            """,
            tools=[],
            agent=agent,
            expected_output="""
                A short, clear recommendation:
                - If suitable: "Crop can be grown", with reasoning
                - If unsuitable: "Crop cannot be grown", with reasons and alternatives
            """
        )




##################################################################################################
# Task 7        page 2
##################################################################################################
    def Final_Advisory_Task(self, agent, comparison_output, soil_weather_output):
        return Task(
            description=f"""
                Generate a polite, concise advisory for the farmer by combining:

                1. Crop Comparison Output: {comparison_output}
                2. Soil & Weather Analysis Output: {soil_weather_output}

                The agent should:
                - Respond in Roman Urdu
                - Explain politely whether the crop is suitable
                - Suggest alternatives if necessary
                - Keep the message short, clear, and farmer-friendly
            """,
            tools=[],
            agent=agent,
            expected_output="""
                A final advisory message in Roman Urdu:
                - Polite and encouraging
                - Short and to the point
                - Includes reasoning from both comparison and soil/weather suitability
            """
        )








##################################################################################################
# Task 8       page 3
##################################################################################################
    def Irrigation_Priority_Weather_Task(self, agent, farmers_data):
        """
        farmers_data = [
            {
                "name": "Kisan 1",
                "crop": "Tomato",
                "soil_data": {"moisture": 18, "pH": 6.5},
                "weather_data": {"risk": "Heatwave", "temperature": 34, "humidity": 30, "rainfall_mm": 0}
            },
            {
                "name": "Kisan 2",
                "crop": "Spinach",
                "soil_data": {"moisture": 30, "pH": 6.8},
                "weather_data": {"risk": "Normal", "temperature": 28, "humidity": 50, "rainfall_mm": 2}
            },
            ...
        ]
        """
        return Task(
            description=f"""
                4 kisanon ke soil aur weather data ko analyze karke irrigation priority tayar karein.  

                Har kisan ka data:
                {farmers_data}

                Agent ka kaam:
                - Soil moisture, pH aur weather data (risk, temperature, humidity, rainfall_mm) ka analysis karein
                - Crop ki irrigation needs ko samajhkar priority decide karein
                - 1 se 4 tak ranking dein: kaun sab se pehle paani de, kaun doosre, teesre aur aakhri
                - Har kisan ke liye short reasoning Roman Urdu mein dein
                - Output friendly aur clear ho, koi emoji ya complex term na ho
            """,

            tools=[],
            agent=agent,

            expected_output="""
                Roman Urdu mein output format:

                1. Kisan 1 (Tomato) - Zameen ka moisture 18% hai aur mausam Heatwave hai, temperature 34°C. Pehle paani dena zaroori.
                2. Kisan 3 (Carrot) - Moisture 20%, Mausam Flood Risk. Doosre number par paani dena chahiye.
                3. Kisan 4 (Cucumber) - Moisture 25%, Normal conditions. Third priority.
                4. Kisan 2 (Spinach) - Moisture 30%, Normal conditions. Aakhri priority.
            """
        )
    




##################################################################################################
# Task 9 - Season Aware Harvest Prediction
##################################################################################################
    def Harvest_Prediction_Task_Seasonal(self, agent, farmers_data, current_date):
    
        return Task(
            description=f"""
                Har kisan ke crop ka analysis karein aur season ke hisaab se determine karein:
                - Current date se season detect karein (Spring, Summer, Autumn, Winter)
                - Check karein ke har crop is season me harvest hoti hai ya nahi
                - Jo crops harvest ke liye ready hain, unko tools priority wise assign karein
                - Tools priority assign karte waqt reason bhi explain karein (soil, crop type, maturity, season match)

                Parameters:
                - Farmers Data: {farmers_data}
                - Current Date: {current_date}

                Agent ka kaam:
                1. Current date se season identify karein
                2. Har crop ki usual harvesting season se match karein
                3. Jo crops is season me cut ho sakti hain, unko pehle tools assign karein
                4. Baqi crops ko baad me assign karein
                5. Har farmer ke liye short, clear, polite aur reasoning ke saath Roman Urdu response dein
            """,

            tools=[],
            agent=agent,

            expected_output="""
                Roman Urdu mein output example with reasoning:

                1. Kisan 1 (Wheat) - Current season: Autumn. Wheat is fully mature and harvest ke liye ready hai. Soil moisture aur weather conditions perfect hain. Tools pehle allocate karein: Sickle, Tractor. Reason: Wheat harvest ke liye is season me best condition me hai.
                2. Kisan 3 (Rice) - Current season: Autumn. Rice harvest ke liye thoda sa der me ready hoga. Soil moisture adequate hai. Tools doosre priority par: Harvester. Reason: Crop almost ready hai, thoda wait karne ke baad tools use karein.
                3. Kisan 2 (Corn) - Current season: Autumn. Corn abhi mature nahi hui. Tools teesre priority par: Tractor. Reason: Corn thodi der baad ready hoga, abhi tools unnecessary hain.
                4. Kisan 4 (Spinach) - Current season: Autumn. Abhi harvest ke liye ready nahi. Tools last priority. Reason: Crop immature hai, tools abhi allocate karna waste hoga.
            """
        )



##################################################################################################
# Task 10 - Pest Advisor Task
##################################################################################################
    def Pest_Advisor_Task(self, agent, farmers_data):
        return Task(
            description=f"""
                Har farmer ke farm ka pest detection check karein aur unko solution provide karein.
                
                Agent ka kaam:
                1. Farmers data me se 'pest_detection' key check karein
                2. Agar pest 'None' hai: "Koi pest nahi hai" response dein
                3. Agar pest hai: 
                - Locust: traps, neem oil, ya pesticide use ka short solution
                - Bollworm: Bt spray, remove infected bolls
                - Armyworm: manual removal, neem spray
                4. Har solution Roman Urdu me concise aur polite hona chahiye
                
                Parameters:
                - pest detection: {farmers_data}
            """,
            
            tools=[],
            agent=agent,
            
            expected_output="""
                Roman Urdu output example:
                
                1. Kisan 1 - Pest: None. Koi pest nahi hai, abhi koi action ki zarurat nahi.
                2. Kisan 2 - Pest: Locust. Locust attack ka risk hai. Fasal ke aas paas traps lagayein aur neem oil ka spray karein. Agar severe ho, authorized pesticide use karein.
                3. Kisan 3 - Pest: Bollworm. Infested cotton bolls ko remove karein aur Bt spray karein. Chemical pesticide sirf zarurat par use karein.
                4. Kisan 4 - Pest: Armyworm. Manual removal karein ya neem-based insecticide apply karein. Daily monitoring zaruri hai.
            """
        )
    

##################################################################################################
# Task 11 - Unified Farmer Summary Task
##################################################################################################
    def Farmer_Summary_Advisor_Task(self, agent, irrigation_output, harvest_output, pest_output, rag_output):
        return Task(
            description=f"""
                Agent ko chaar agents ke outputs provide karein:
                1. Irrigation Priority & Weather Analysis
                2. Harvest Prediction Seasonal
                3. Pest Advisor
                4. Market demand & prices (city-wise)

                Agent ka kaam:
                - Saare outputs ko analyze karein
                - Har farmer ke liye ek concise, polite, Roman Urdu advisory generate karein
                - Advisory structured aur detailed ho:
                    * Irrigation: Priority level (High, Medium, Low) assign karein aur wajah bhi batayen 
                    (jaise zameen dry hai, mosam garam hai, pani ka level low hai, etc.)
                    * Harvesting: Fasal ready hai ya nahi, aur approx kitne din baad ready hogi agar abhi nahi
                    * Pests: Agar pest detected ho to uska clear solution batayen
                    * Market: City-wise demand aur best selling price highlight karein (kis city me zyada demand hai aur rate kitna hai)

                Parameters:
                - Irrigation Output: {irrigation_output}
                - Harvest Output: {harvest_output}
                - Pest Output: {pest_output}
                - Market demand and prices: {rag_output}
            """,

            tools=[],
            agent=agent,

            expected_output="""
                Roman Urdu output example:

                1. Kisan 1 - 
                Irrigation: High priority, zameen dry hai aur temperature high hai, is liye aaj paani dena zaroori hai. 
                Harvesting: Wheat harvest ready hai. 
                Pest: Koi pest nahi mila. 
                Market: Lahore me wheat ki demand high hai, price Rs. 2500/qtl, Multan me price Rs. 2400/qtl.

                2. Kisan 2 - 
                Irrigation: Low priority, zameen moist hai aur mosam cloudy hai, is liye abhi paani dena zaroori nahi. 
                Harvesting: Corn harvest 10 din baad ready hoga. 
                Pest: Locust attack ka risk hai, neem oil ka spray karein. 
                Market: Faisalabad me corn ki demand medium hai, price Rs. 1800/qtl, Karachi me demand low hai Rs. 1700/qtl.

                3. Kisan 3 - 
                Irrigation: Medium priority, zameen thodi dry hai lekin mosam thoda thanda hai, is liye kal tak paani dena theek hoga. 
                Harvesting: Rice harvest ready hai. 
                Pest: Bollworm detected, infested bolls remove karein aur Bt spray karein. 
                Market: Karachi me rice ki demand high hai Rs. 3000/qtl, Lahore me demand medium hai Rs. 2900/qtl.

                4. Kisan 4 - 
                Irrigation: Low priority, zameen wet hai aur rainfall expected hai. 
                Harvesting: Spinach harvest abhi ready nahi, approx 7 din baad. 
                Pest: Armyworm detected, manual removal ya neem spray karein. 
                Market: Lahore me spinach demand low hai Rs. 50/kg, Rawalpindi me medium demand hai Rs. 60/kg.
            """
        )
