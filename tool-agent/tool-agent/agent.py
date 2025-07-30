from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="tool_agent",  
    model="gemini-2.0-flash",
    description="Tool Agent",
    instruction=""" You are a helpful assistant that can use following tools to assist users:
    google_search
    """,
    tools=[google_search],
    )