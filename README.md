# Deep Agents Tutorial
A hands-on tutorial building a Competitive Intelligence Agent 
using LangChain's Deep Agents framework + OpenAI + Streamlit.

## What it does
Type a research query. The agent plans tasks, spawns subagents 
per competitor, searches the web, and writes a structured report.

## Stack
- LangChain `deepagents` — agent harness built on LangGraph
- OpenAI `gpt-4o-mini` — the model
- Tavily — web search
- Streamlit — UI

## Quickstart
- Create a Python virtual environment (Run `python -m venv .venv` & then activate it using `source .venv/bin/activate`)
- Then install dependencies using `pip install -r requirements.txt`
- Add your OPENAI_API_KEY and TAVILY_API_KEY to .env (You need to create a .env file and then add both API keys)
- Run the app using `streamlit run app.py`

## Reference
Built following the official LangChain Deep Agents documentation.
https://docs.langchain.com/oss/python/deepagents/overview
