from llama_index.core import StorageContext, ServiceContext, load_index_from_storage
from llama_index.core.callbacks.base import CallbackManager
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.groq import Groq
from llama_index.postprocessor.cohere_rerank import CohereRerank
import os
from dotenv import load_dotenv
load_dotenv()
import chainlit as cl

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

@cl.on_chat_start
async def factory():
    storage_context = StorageContext.from_defaults(persist_dir="./storage")

    embed_model = GeminiEmbedding(
        model_name="models/embedding-001", api_key=GOOGLE_API_KEY
    ) 

    llm = Groq(model="mixtral-8x7b-32768", api_key=GROQ_API_KEY)

    service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm,
                        callback_manager=CallbackManager([cl.LlamaIndexCallbackHandler()]),
    )
    cohere_rerank = CohereRerank(api_key=COHERE_API_KEY, top_n=2)

    index = load_index_from_storage(storage_context, service_context=service_context)

    query_engine = index.as_query_engine(
        service_context=service_context,
        similarity_top_k=10,
        node_postprocessors=[cohere_rerank],
        # streaming=True,
    )

    cl.user_session.set("query_engine", query_engine)

@cl.on_message
async def main(message: cl.Message):
    query_engine = cl.user_session.get("query_engine")  
    response = await cl.make_async(query_engine.query)(message.content)

    response_message = cl.Message(content="")

    for token in response.response:
        await response_message.stream_token(token=token)

    # if response.response_txt:
    #     response_message.content = response.response_txt

    await response_message.send()
