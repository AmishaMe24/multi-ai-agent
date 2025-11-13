from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch

from langchain.agents import create_agent
from langchain_core.messages.ai import AIMessage

from app.config.settings import settings

def get_response_from_ai_agents(model_name, query, allow_search, system_prompt):
    llm = ChatGroq(model=model_name, temperature=0)

    tools = [TavilySearch(max_results=2)] if allow_search else []

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )

    state = {"messages": query}

    response = agent.invoke(state)
    messages = response.get("messages")
    ai_messages = [messages.content for messages in messages if isinstance(messages, AIMessage)]
    return ai_messages[-1]


