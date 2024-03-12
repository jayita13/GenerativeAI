import chainlit as cl
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=groq_api_key,
)

@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message.content,
            }
        ],
        model="mixtral-8x7b-32768",
    )

    # Send a response back to the user
    await cl.Message(
        content=f"{chat_completion.choices[0].message.content}",
    ).send()

