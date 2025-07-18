# Import core components from the OpenAI Agents SDK
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, Runner, set_tracing_export_api_key, function_tool, RunContextWrapper
from agents.model_settings import ModelSettings

# For loading environment variables from a .env file
from dotenv import load_dotenv, find_dotenv
import os
import asyncio

# Pydantic model for type-safe user context
from pydantic import BaseModel

# Load environment variables
load_dotenv(find_dotenv())

# Get API keys from .env
api_key = os.getenv("GEMINI_API_KEY")
set_tracing_export_api_key(os.getenv("OPENAI_API_KEY"))  # Used for OpenAI tracing dashboard

# Create a client for Gemini-compatible chat API
client = AsyncOpenAI(
    api_key=api_key,
    base_url= os.getenv("BASE_URL")  # Base URL for Gemini model if different from OpenAI's
)

# Define the context schema passed during runs
class user_details(BaseModel):
    is_premium: bool  # User subscription status

# Define the chat model used by agents (Gemini here)
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

# Define a tool for fetching weather info
@function_tool
def get_weather(city: str):
    return f"The weather in {city} is sunny"

# Define a tool for fetching temperature info
@function_tool
def get_temprature(city: str):
    return f"The temperature in {city} is 38C"

# Dynamic instruction generator based on user context
def dynamic_instructions(context: RunContextWrapper[user_details], agent: Agent):
    if context.context.is_premium:
        # Premium user gets full functionality
        return """You are a helping agent and your task 
                  is to fulfill user requirements and perform relevant
                  task like tool calls, handoffs and etc"""
    
    # Non-premium user gets a limited response with upsell message
    return """You are a helping agent and your task is to
               fulfill user requirements and perform relevant tasks
               but since he is not premium don't offer refund
               and ask to purchase premium of 10$"""

# Define a refund agent (used for handoffs)
refund_agent = Agent(
    name="Refund Agent",
    instructions="You are a refunding agent",
    model=model
)

# Main helping agent that uses tools and may hand off
helping_agent = Agent(
    name="Helping Agent",
    instructions=dynamic_instructions,  # Dynamic based on context
    model_settings=ModelSettings(tool_choice="required"),  # Force tool usage
    reset_tool_choice=True,  # Reset after each turn
    tool_use_behavior="stop_on_first_tool",  # Stop once a tool is used
    tools=[get_weather, get_temprature],  # Registered tools
    handoffs=[refund_agent],  # Possible handoff agents
    model=model
)

# Async function to run the agent
async def output():
    # Create user context with is_premium = False
    user_det = user_details(is_premium=False)

    # Start the run with helping_agent and user input
    result = await Runner.run(
        starting_agent=helping_agent,
        input="What is weather and temprature in lahore",
        context=user_det
    )

    # Print the final output after tool use and/or handoff
    print(result.final_output)

# Run the async output function when script is executed directly
if __name__ == "__main__":
    asyncio.run(output())
