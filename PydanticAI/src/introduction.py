"""
Introduction to PydanticAI.

This module demonstrates how PydanticAI makes it easier to build
production-grade LLM-powered systems with type safety and structured responses.
"""

from typing import Dict, List, Optional
import nest_asyncio
from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel
from utils.markdown import to_markdown
from dotenv import load_dotenv
load_dotenv()
nest_asyncio.apply()

model = OpenAIModel("gpt-4o")

# --------------------------------------------------------------
# 1. Simple Agent - Hello World Example
# --------------------------------------------------------------
"""
This example demonstrates the basic usage of PydanticAI agents.
Key concepts:
- Creating a basic agent with a system prompt
- Running synchronous queries
- Accessing response data, message history, and costs
"""

agent1 = Agent(
    model=model,
    system_prompt="You are a helpful customer support agent. Be concise and friendly.",
)

# Example usage of basic agent
response = agent1.run_sync("How can I track my order #12345?")
print(response.data)
print(response.all_messages())
# print(response.cost())


response2 = agent1.run_sync(
    user_prompt="What was my previous question?",
    message_history=response.new_messages(),
)
print(response2.data)

# --------------------------------------------------------------
# 2. Agent with Structured Response
# --------------------------------------------------------------
"""
This example shows how to get structured, type-safe responses from the agent.
Key concepts:
- Using Pydantic models to define response structure
- Type validation and safety
- Field descriptions for better model understanding
"""


class ResponseModel(BaseModel):
    """Structured response with metadata."""

    response: str
    needs_escalation: bool
    follow_up_required: bool
    sentiment: str = Field(description="Customer sentiment analysis")


agent2 = Agent(
    model=model,
    result_type=ResponseModel,
    system_prompt=(
        "You are an intelligent customer support agent. "
        "Analyze queries carefully and provide structured responses."
    ),
)

response = agent2.run_sync("How can I track my order #12345?")
print(response.data.model_dump_json(indent=2))


# --------------------------------------------------------------
# 3. Agent with Structured Response & Dependencies
# --------------------------------------------------------------
"""
This example demonstrates how to use dependencies and context in agents.
Key concepts:
- Defining complex data models with Pydantic
- Injecting runtime dependencies
- Using dynamic system prompts
"""


# Define order schema
class Order(BaseModel):
    """Structure for order details."""

    order_id: str
    status: str
    items: List[str]


# Define customer schema
class CustomerDetails(BaseModel):
    """Structure for incoming customer queries."""

    customer_id: str
    name: str
    email: str
    orders: Optional[List[Order]] = None


# Agent with structured output and dependencies
agent5 = Agent(
    model=model,
    result_type=ResponseModel,
    deps_type=CustomerDetails,
    retries=3,
    system_prompt=(
        "You are an intelligent customer support agent. "
        "Analyze queries carefully and provide structured responses. "
        "Always great the customer and provide a helpful response."
    ),  # These are known when writing the code
)


# Add dynamic system prompt based on dependencies
@agent5.system_prompt
async def add_customer_name(ctx: RunContext[CustomerDetails]) -> str:
    return f"Customer details: {to_markdown(ctx.deps)}"  # These depend in some way on context that isn't known until runtime


customer = CustomerDetails(
    customer_id="1",
    name="John Doe",
    email="john.doe@example.com",
    orders=[
        Order(order_id="12345", status="shipped", items=["Blue Jeans", "T-Shirt"]),
    ],
)

response = agent5.run_sync(user_prompt="What did I order?", deps=customer)

response.all_messages()
print(response.data.model_dump_json(indent=2))

print(
    "Customer Details:\n"
    f"Name: {customer.name}\n"
    f"Email: {customer.email}\n\n"
    "Response Details:\n"
    f"{response.data.response}\n\n"
    "Status:\n"
    f"Follow-up Required: {response.data.follow_up_required}\n"
    f"Needs Escalation: {response.data.needs_escalation}"
)


# --------------------------------------------------------------
# 4. Agent with Tools
# --------------------------------------------------------------

"""
This example shows how to enhance agents with custom tools.
Key concepts:
- Creating and registering tools
- Accessing context in tools
"""

shipping_info_db: Dict[str, str] = {
    "12345": "Shipped on 2024-12-01",
    "67890": "Out for delivery",
}


def get_shipping_info(ctx: RunContext[CustomerDetails]) -> str:
    """Get the customer's shipping information."""
    return shipping_info_db[ctx.deps.orders[0].order_id]


# Agent with structured output and dependencies
agent5 = Agent(
    model=model,
    result_type=ResponseModel,
    deps_type=CustomerDetails,
    retries=3,
    system_prompt=(
        "You are an intelligent customer support agent. "
        "Analyze queries carefully and provide structured responses. "
        "Use tools to look up relevant information."
        "Always great the customer and provide a helpful response."
    ),  # These are known when writing the code
    tools=[Tool(get_shipping_info, takes_ctx=True)],  # Add tool via kwarg
)


@agent5.system_prompt
async def add_customer_name(ctx: RunContext[CustomerDetails]) -> str:
    return f"Customer details: {to_markdown(ctx.deps)}"


response = agent5.run_sync(
    user_prompt="What's the status of my last order?", deps=customer
)

response.all_messages()
print(response.data.model_dump_json(indent=2))

print(
    "Customer Details:\n"
    f"Name: {customer.name}\n"
    f"Email: {customer.email}\n\n"
    "Response Details:\n"
    f"{response.data.response}\n\n"
    "Status:\n"
    f"Follow-up Required: {response.data.follow_up_required}\n"
    f"Needs Escalation: {response.data.needs_escalation}"
)


# --------------------------------------------------------------
# 5. Agent with Reflection and Self-Correction
# --------------------------------------------------------------

"""
This example demonstrates advanced agent capabilities with self-correction.
Key concepts:
- Implementing self-reflection
- Handling errors gracefully with retries
- Using ModelRetry for automatic retries
- Decorator-based tool registration
"""

# Simulated database of shipping information
shipping_info_db: Dict[str, str] = {
    "#12345": "Shipped on 2024-12-01",
    "#67890": "Out for delivery",
}

customer = CustomerDetails(
    customer_id="1",
    name="John Doe",
    email="john.doe@example.com",
)

# Agent with reflection and self-correction
agent5 = Agent(
    model=model,
    result_type=ResponseModel,
    deps_type=CustomerDetails,
    retries=3,
    system_prompt=(
        "You are an intelligent customer support agent. "
        "Analyze queries carefully and provide structured responses. "
        "Use tools to look up relevant information. "
        "Always greet the customer and provide a helpful response."
    ),
)


@agent5.tool_plain()  # Add plain tool via decorator

def get_shipping_status(order_id: str) -> str:
    """Get the shipping status for a given order ID."""
    shipping_status = shipping_info_db.get(order_id)
    if shipping_status is None:
        raise ModelRetry(
            f"No shipping information found for order ID {order_id}. "
            "Make sure the order ID starts with a #: e.g, #624743 "
            "Self-correct this if needed and try again."
        )
    return shipping_info_db[order_id]


# Example usage
response = agent5.run_sync(
    user_prompt="What's the status of my last order 12345?", deps=customer
)

response.all_messages()
print(response.data.model_dump_json(indent=2))
