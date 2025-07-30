from google.adk.agents import Agent
from pydantic import BaseModel, Field

class ParticipantData(BaseModel):
    participantId: str = Field(..., description="Unique identifier for the participant")
    name: str = Field(..., description="Name of the participant")
    age: int = Field(..., description="Age of the participant")
    email: str = Field(..., description="Email address of the participant")
    phoneNo: str = Field(..., description="Phone number of the participant")

root_agent = Agent(
    name="structured_output_agent",
    description="Structured Output Agent gives participant data in a particular JSON format",
    model="gemini-2.0-flash",
    instruction="""
    You are a helpful assistant that provides the following participant data in a structured JSON format.
    A participant id which needs to be randomly generated 8 letters alphanumeric string where letters used are always uppercase letters
    A randomly generated name which contains first name and last name
    A randomly generated age between 18 and 60
    A randomly generated email address
    A randomly generated phone number in the format (XXX) XXX-XXXX
    """,
    output_schema=ParticipantData,
    output_key="participantData"
)