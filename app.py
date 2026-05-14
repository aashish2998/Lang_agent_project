import os
import certifi
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.tools import tool
import requests
from langchain.agents import create_react_agent, AgentExecutor

os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Dark background */
.stApp {
    background-color: #0d0d0d;
    color: #e8e8e8;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Title */
h1 {
    font-family: 'Space Mono', monospace !important;
    font-size: 1.8rem !important;
    color: #f0f0f0 !important;
    letter-spacing: -0.5px;
    margin-bottom: 0 !important;
}

/* Subtitle */
.subtitle {
    font-size: 0.82rem;
    color: #555;
    font-family: 'Space Mono', monospace;
    margin-bottom: 2rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Input */
.stTextArea textarea {
    background-color: #161616 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
    color: #e0e0e0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    border-color: #4ade80 !important;
    box-shadow: 0 0 0 2px rgba(74,222,128,0.12) !important;
}

/* Button */
.stButton > button {
    background: #4ade80 !important;
    color: #0d0d0d !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.55rem 1.6rem !important;
    transition: opacity 0.15s ease !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
}

/* Output card */
.output-card {
    background: #161616;
    border: 1px solid #222;
    border-left: 3px solid #4ade80;
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    margin-top: 1rem;
    font-size: 0.95rem;
    line-height: 1.7;
    color: #d4d4d4;
    white-space: pre-wrap;
}

/* Chips row */
.chip-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}
.chip {
    background: #1a1a1a;
    border: 1px solid #2e2e2e;
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.72rem;
    color: #888;
    font-family: 'Space Mono', monospace;
    cursor: pointer;
    transition: border-color 0.15s, color 0.15s;
}
.chip:hover { border-color: #4ade80; color: #4ade80; }

/* Spinner override */
.stSpinner > div { border-top-color: #4ade80 !important; }

/* Label */
label { color: #666 !important; font-size: 0.78rem !important; letter-spacing: 0.5px; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)


# ── Agent setup (cached) ──────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def build_agent():
    search_tool = TavilySearchResults(max_results=2)

    @tool
    def get_weather_data(city: str) -> str:
        """Fetch current weather information for a city."""
        url = (
            f"https://api.weatherstack.com/current?"
            f"access_key={WEATHERSTACK_API_KEY}&query={city}"
        )
        data = requests.get(url).json()
        if "current" not in data:
            return f"Could not fetch weather data for {city}"
        return (
            f"City: {city}\n"
            f"Temperature: {data['current']['temperature']}°C\n"
            f"Weather: {data['current']['weather_descriptions'][0]}\n"
            f"Humidity: {data['current']['humidity']}%"
        )

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile",
        temperature=0,
    )
    tools = [search_tool, get_weather_data]
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)


# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("# 🤖 AI Agent")
st.markdown('<p class="subtitle">Search · Weather · Anything</p>', unsafe_allow_html=True)

# Quick-prompt chips
EXAMPLES = [
    "Weather in Bangalore right now",
    "Latest news in AI today",
    "Temperature in Tokyo",
    "Top cricket news today",
]

st.markdown(
    '<div class="chip-row">' +
    "".join(f'<span class="chip" onclick="void(0)">⚡ {e}</span>' for e in EXAMPLES) +
    "</div>",
    unsafe_allow_html=True,
)

# Input
query = st.text_area(
    "Your question",
    placeholder="Ask anything — weather, search, news…",
    height=100,
    label_visibility="collapsed",
)

# Column layout for button + hint
col1, col2 = st.columns([1, 4])
with col1:
    run = st.button("RUN →")
with col2:
    st.markdown(
        "<p style='color:#333;font-size:0.72rem;margin-top:0.6rem;font-family:Space Mono,monospace;'>GROQ · TAVILY · WEATHERSTACK</p>",
        unsafe_allow_html=True,
    )

# Run agent
if run:
    if not query.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Thinking…"):
            try:
                executor = build_agent()
                result = executor.invoke({"input": query.strip()})
                output = result.get("output", "No response returned.")
            except Exception as e:
                output = f"Error: {e}"

        st.markdown(f'<div class="output-card">{output}</div>', unsafe_allow_html=True)