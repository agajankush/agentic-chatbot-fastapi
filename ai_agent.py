# 1. SetupAPI for GROQ and Tavily
import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# 2. Setup LLM & Tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

# openai_llm=ChatOpenAI(model_name="gpt-4o-mini")
groq_llm=ChatGroq(model_name="llama-3.3-70b-versatile")

search_tool=TavilySearchResults(max_results=2)

# 3. Setup AI Agent with Search tool functionality
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

system_prompt="Act as a Customer service representative for SASS platform who is smart and friendly"

def get_response(llm_id, query, allow_search, system_prompt, provider):
    if provider == "Groq":
        llm=ChatGroq(model=llm_id)
    elif provider == "OpenAI":
        llm=ChatOpenAI(model=llm_id)
    
    tools=[TavilySearchResults(max_results=2)] if allow_search else []
    agent=create_react_agent(
        model=groq_llm,
        tools=tools,
        state_modifier=system_prompt
    )

    # Invoking
    state={"messages": query}
    response=agent.invoke(state)
    messages = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]
