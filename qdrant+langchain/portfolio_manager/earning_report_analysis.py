import os
from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain_community.vectorstores import Qdrant

import qdrant_client

# portfolio_summarizer_constants is the constants file which contains 
# these 2 variables.
from portfolio_constants import VECTOR_DB_COLLECTION, portfolio

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

CHUNK_SIZE = 1500
CHUNK_OVERLAP = 300
LATEST_EARNINGS_QUARTER = "Q3"
LATEST_EARNINGS_YEAR = "2023"

llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )
Embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Queries the database to fetch the earnings report of the company
def get_earnings_from_vector_store(portfolio_stock):
    company_name = portfolio_stock["company_name"]
    question = "Get the quarterly earning report of " + company_name + """ Get the information like Revenue, 
            Earnings, Net Income, Expenses, Cash Flow, Guidance, Market Conditions, Growth Drivers, 
            Challenges and Management Outlook"""

    source_info = generate_db_source_info(portfolio_stock)
    qdrant_retriever = get_qdrant_retriever(source_info);
    result_docs = qdrant_retriever.get_relevant_documents(question)
    print("Number of documents found: ", len(result_docs))

    retrieved_text = ""
    for i in range(len(result_docs)):
        retrieved_text += result_docs[i].page_content

    return retrieved_text


# Generating the source filter which will be used as filter when querying the vector store for better query results
def generate_db_source_info(entry):
    ticker = entry["ticker"]
    return ticker + "-" + LATEST_EARNINGS_QUARTER + "-" + LATEST_EARNINGS_YEAR


# Generates the Qdrant retriever object
def get_qdrant_retriever(source_info):
    qdrant_client_obj = qdrant_client.QdrantClient(
        url=QDRANT_URL,
        prefer_grpc=True,
        api_key=QDRANT_API_KEY)
    qdrant = Qdrant(qdrant_client_obj, VECTOR_DB_COLLECTION, Embeddings)
    return qdrant.as_retriever(search_kwargs={'filter': {'source': source_info}, 'k': 2})


# This function is an orchestrator function which controls the flow, first it calls the Qdrant vector store to get
# earnings report of the company. Next it passes the fetched earning report to the LLM to perform analysis.
def report_analysis(portfolio_stock):
    company_name = portfolio_stock["company_name"]
    template = "You are a stock analyst analyzing " + company_name + "'s quarterly earnings report." + """
        Based on the report summarize the sentiment towards the company and its performance. Identify \
        key positive and negative aspects, focusing on financial results, future outlook, and investment potential. 

        Additionally, answer the following questions:
        1/ Does the company meet or exceed analyst expectations? 
        2/ What are the main risks and opportunities facing the company in the coming year?

        Below is the earnings report:

        {earnings_report}
    """

    earnings_report = get_earnings_from_vector_store(portfolio_stock)
    print("Generating Analysis for " + company_name)

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    return chain.invoke({"earnings_report": earnings_report}).content


# Performs Earning Analysis of a single company
def get_company_analysis(company_name):
    print("Selected company: ", company_name)
    portfolio_stock = None
    for entry in portfolio:
        if entry["company_name"] == company_name:
            portfolio_stock = entry
            break
    analysed_report = report_analysis(portfolio_stock)
    print("Analysis by LLM: ", analysed_report)
    return analysed_report