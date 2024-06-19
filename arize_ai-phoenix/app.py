from llama_index.core import StorageContext, ServiceContext, load_index_from_storage
from llama_index.core.callbacks.base import CallbackManager
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
import chainlit as cl

# Phoenix can display in real time the traces automatically
# collected from your LlamaIndex application.
import phoenix as px
# Look for a URL in the output to open the App in a browser.
px.launch_app()
# The App is initially empty, but as you proceed with the steps below,
# traces will appear automatically as your LlamaIndex application runs.

from llama_index.core import set_global_handler

set_global_handler("arize_phoenix")

# Run all of your LlamaIndex applications as usual and traces
# will be collected and displayed in Phoenix.

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@cl.on_chat_start
async def factory():
    storage_context = StorageContext.from_defaults(persist_dir="./storage_mini")

    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    llm = Groq(model="llama3-70b-8192", api_key=GROQ_API_KEY)

    service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm,
                        callback_manager=CallbackManager([cl.LlamaIndexCallbackHandler()]),
    )

    index = load_index_from_storage(storage_context, service_context=service_context)

    chat_engine = index.as_chat_engine(service_context=service_context)

    cl.user_session.set("chat_engine", chat_engine)

@cl.on_message
async def main(message: cl.Message):
    chat_engine = cl.user_session.get("chat_engine")  
    response = await cl.make_async(chat_engine.chat)(message.content)

    response_message = cl.Message(content="")

    for token in response.response:
        await response_message.stream_token(token=token)

    await response_message.send()
