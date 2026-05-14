import os
import certifi



from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.tools import tool
import requests
from langchain.agents import create_react_agent, AgentExecutor
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()



GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")     


search_tool = TavilySearchResults(max_results=1)
@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a city.
    """

    url = (
        f"https://api.weatherstack.com/current?"
        f"access_key={WEATHERSTACK_API_KEY}&query={city}"
    )

    response = requests.get(url)

    data = response.json()

    if "current" not in data:
        return f"Could not fetch weather data for {city}"

    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%"
    )
result = search_tool.invoke('what is today"s weather')
result
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile", # This model is free, fast, and smart
    temperature=0
)
response = llm.invoke('When was the first icc tournament')

response 
prompt = hub.pull("hwchase17/react")
prompt
tools = [search_tool, get_weather_data]
# ==========================================
# CREATE AGENT
# ==========================================

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)
# EXECUTOR
# ==========================================

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True   # used to se the logs of the agent
)
response = agent_executor.invoke({
    "input": (
        #"India's Tea garden in himachal"
        "Current weather and temperature in Kangra"
        
    )
})

print("FINAL OUTPUT")
print(response['output'])