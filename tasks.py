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
    def Irrigation_Advisory_Task(self, agent, soil_data, weather_data, vegetable_name):
        return Task(
            description=f"""
                Analyze the given soil and weather data along with the vegetable name to decide
                whether watering (pani dena) is needed or not.

                Inputs:
                1. Soil Data: {soil_data}
                2. Weather Data: {weather_data}
                3. Vegetable Name: {vegetable_name}

                The agent should:
                - Study soil moisture, temperature, and humidity
                - Consider the water requirement of the given vegetable
                - Factor in the weather condition (e.g., agar garmi zyada ho to pani jaldi zaroori ho sakta hai)
                - Decide if pani dena abhi zaroori hai ya kuch der baad
                - Mention roughly kitni der mein pani dena chahiye (agar zarurat ho)
                - Reply in **clear, polite Roman Urdu**, easy for a farmer to understand
            """,
            tools=[],
            agent=agent,
            expected_output="""
                A short and polite irrigation advisory message in Roman Urdu:
                - Mentions whether vegetable needs water or not
                - If needed, tells how soon pani dena chahiye (e.g., "agli 2 ghanton mein pani dena zaroori hai")
                - If not needed, tells for how long there’s no need (e.g., "agli 6 ghante tak pani ki koi zarurat nahi")
                - Takes both soil and weather conditions into account
            """
        )
