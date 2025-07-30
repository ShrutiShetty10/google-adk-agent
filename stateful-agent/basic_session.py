from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.genai import types
import asyncio

load_dotenv()  # Load environment variables if needed
# Define agent with output_key
greeting_agent = LlmAgent(
    name="Greeter",
    model="gemini-2.0-flash", # Use a valid model
    instruction="""
    You are a friendly quetion answering agent. Answer the question based on the user's preferences." \
    Name: 
    {user_name}
    Preferences: 
    {user_preferences}
    """,
    output_key="last_greeting" # Save response to state['last_greeting']
)
async def main():
    # --- Create Session Service ---
    # InMemorySessionService is used for demonstration; replace with your session service
    session_service = InMemorySessionService()
    initial_state = {
        "user_name": "Jane Doe",
        "user_preferences": "My favorite sports are soccer and basketball.",
    }
    # --- Create Session ---
    app_name, user_id, session_id = "greeting_app", "user1", "session1"
    session = await session_service.create_session(app_name=app_name,
                                                   user_id=user_id,
                                                   session_id=session_id,
                                                   state=initial_state)
    print(f"Initial state: {session.user_id} - {session.id}")
    # --- Setup Runner and Session ---
    runner = Runner(
        agent=greeting_agent,
        app_name=app_name,
        session_service=session_service
    )

    # --- Run the Agent ---
    # Runner handles calling append_event, which uses the output_key
    # to automatically create the state_delta.
    user_message = types.Content(
    role="user", parts=[types.Part(text="What is Jane's favorite sports?")]
)
   # user_message = Content(parts=[Part(text="Whats Jane Doe's hobbies?")])
    print("==== Running Agent ====")
    for event in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message= user_message,
    ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    print(f"Final Response: {event.content.parts[0].text}") # Response text is also in event.content

    # --- Check Updated State ---
    updated_session = await session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
    print(f"State after agent run: {updated_session.state}")
    # Expected output might include: {'last_greeting': 'Hello there! How can I help you today?'}

asyncio.run(main())