from google.adk.agents import Agent

root_agent = Agent(
    name="greeting_agent",  
    model="gemini-2.0-flash",
    description="Greeting Agent",
    instruction=""" You are a helpful assistant that greets users 
    and asks them about their day.
    """
    )