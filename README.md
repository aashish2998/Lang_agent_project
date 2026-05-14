# Lang_agent_project
First AI Agent project - Search and find Current weather  using Langchain

# 🤖 LangChain AI Agent — Search & Weather

A ReAct-based AI agent built with **LangChain** + **Groq (LLaMA 3.3 70B)** that can intelligently search the web and fetch real-time weather data. Comes with a clean **Streamlit UI** for interactive use.

---

## 📌 What This Project Does

This agent uses the **ReAct (Reasoning + Acting)** pattern — it thinks step by step, decides which tool to use, calls it, observes the result, and responds. You ask a question in plain English; the agent figures out whether to search the web, check the weather, or both.

**Example queries:**
- `"Current weather and temperature in Kangra"`
- `"Latest news about AI in India"`
- `"Weather in Mumbai and recent news about the city"`

---

## 🏗️ Architecture

```
User Query
    │
    ▼
AgentExecutor (ReAct loop)
    │
    ├──► TavilySearchResults   → Web search (news, facts, general queries)
    │
    └──► get_weather_data()    → Weatherstack API (real-time weather by city)
    │
    ▼
LLaMA 3.3 70B via Groq
    │
    ▼
Final Answer
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | LLaMA 3.3 70B (via Groq) |
| Agent Framework | LangChain ReAct Agent |
| Web Search | Tavily Search API |
| Weather Data | Weatherstack API |
| UI | Streamlit |
| Env Management | python-dotenv |

---

## 📁 Project Structure

```
Lang_agent_project/
├── main.py           # Core agent logic (CLI)
├── app.py            # Streamlit UI
├── requirements.txt  # Dependencies
├── .env              # API keys (not committed)
├── .gitignore        # Ignores .env and other files
├── research/         # Notebooks and experiments
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/aashish2998/Lang_agent_project.git
cd Lang_agent_project
```

### 2. Create a virtual environment
```bash
Steps to Create Virtual Env
conda create -n langagent python=3.11 -y
conda activate langagent
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
WEATHERSTACK_API_KEY=your_weatherstack_api_key
```

> ⚠️ Never commit your `.env` file. It's already listed in `.gitignore`.

---

## 🔑 API Keys — Where to Get Them

| API | Link | Free Tier |
|---|---|---|
| Groq | https://console.groq.com | ✅ Yes |
| Tavily | https://app.tavily.com | ✅ Yes |
| Weatherstack | https://weatherstack.com | ✅ Yes |

---

## 🚀 Running the Project

### Option A — Streamlit UI (recommended)
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

### Option B — Terminal (CLI)
```bash
python main.py
```
Edit the `input` field in `main.py` to change the query.

---

## 🔍 How the ReAct Agent Works

The agent uses the `hwchase17/react` prompt from LangChain Hub, which guides the LLM through this loop:

```
Thought:   What does the user want? What tool should I use?
Action:    Call the appropriate tool (search or weather)
Observation: Read the tool's output
Thought:   Is this enough to answer? Or do I need more?
...repeat if needed...
Final Answer: Provide the complete response
```

This is different from a simple LLM call — the model *reasons* about what to do rather than just generating text.

---

## 📦 Dependencies

```
langchain==0.1.16
langchain-community==0.0.32
langchain-core==0.1.42
langchain-groq
requests==2.31.0
tavily-python
python-dotenv
langchainhub
streamlit
```

---
<img width="1889" height="913" alt="image" src="https://github.com/user-attachments/assets/a83965f5-cb01-4b6f-b9be-a0668b69b6f1" />


## 🌐 Deployment (Render)

This app can be deployed for free on [Render](https://render.com):

1. Push your code to GitHub (without `.env`)
2. Create a new **Web Service** on Render, connect your repo
3. Add environment variables (`GROQ_API_KEY`, `TAVILY_API_KEY`, `WEATHERSTACK_API_KEY`) in Render's dashboard under **Environment**
4. Set the start command to:
   ```bash
   streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```

> Free tier sleeps after 15 min of inactivity. Use [UptimeRobot](https://uptimerobot.com) (free) to keep it alive.

---

## 📚 Reference

This project was built following a hands-on LangChain tutorial on YouTube covering ReAct agents, tool integration, and agent executors.

---

## 📄 License

MIT License — feel free to use, modify, and build on top of this.

---

---
-3 more projects on top of these foundations and your portfolio will be genuinely strong.
