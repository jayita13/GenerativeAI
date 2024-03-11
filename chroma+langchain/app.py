import gradio as gr
import fitz
from PIL import Image
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.llms import Cohere
from langchain.embeddings import CohereEmbeddings
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv
import os
load_dotenv()
COHERE_API_KEY = os.getenv('COHERE_API_KEY')

# Global variables
count = 0
n = 0
chat_history = []
chain = ''

def pdf_reader(pdf_doc):
    
    loader = PyPDFLoader(pdf_doc.name)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)
    db = Chroma.from_documents(texts, embeddings)
    retriever = db.as_retriever()
    chain = ConversationalRetrievalChain.from_llm(Cohere(), retriever=retriever, return_source_documents=True)
    return chain

# Gradio application setup
def create_demo():
    with gr.Blocks(title= " Resume PDF Chatbot",
        theme = "Soft"  # Change the theme here
        ) as demo:
        
        # Create a Gradio block
        with gr.Column():
            with gr.Row():
                chatbot = gr.Chatbot(value=[], elem_id='chatbot', height=680)
                show_img = gr.Image(label='PDF Preview', tool='select', height=680)

        with gr.Row():
            with gr.Column(scale=0.60):
                text_input = gr.Textbox(
                    show_label=False,
                    placeholder="Ask your pdf?",
                container=False)

            with gr.Column(scale=0.20):
                submit_btn = gr.Button('Send')

            with gr.Column(scale=0.20):
                upload_btn = gr.UploadButton("📁 Upload PDF", file_types=[".pdf"])                

        return demo, chatbot, show_img, text_input, submit_btn, upload_btn

# Function to add text to the chat history
def add_text(history, text):
    """
    Adds the user's input text to the chat history.

    Args:
        history (list): List of tuples representing the chat history.
        text (str): The user's input text.

    Returns:
        list: Updated chat history with the new user input.
    """
    if not text:
        raise gr.Error('Enter text')
    history.append((text, ''))
    return history

# Function to generate a response based on the chat history and query
def generate_response(history, query, btn):
    """
    Generates a response based on the chat history and user's query.

    Args:
        history (list): List of tuples representing the chat history.
        query (str): The user's query.
        btn (FileStorage): The uploaded PDF file.

    Returns:
        tuple: Updated chat history with the generated response and the next page number.
    """
    global count, n, chat_history, chain

    if not btn:
        raise gr.Error(message='Upload a PDF')
    if count == 0:
        chain = pdf_reader(btn)
        count += 1

    result = chain({"question": query, 'chat_history': chat_history}, return_only_outputs=True)
    chat_history.append((query, result["answer"]))
    n = list(result['source_documents'][0])[1][1]['page']

    for char in result['answer']:
        history[-1][-1] += char
    return history, " "

    
def render_file(file):
    """
    Renders a specific page of a PDF file as an image.

    Args:
        file (FileStorage): The PDF file.

    Returns:
        PIL.Image.Image: The rendered page as an image.
    """
    global n
    doc = fitz.open(file.name)
    page = doc[n]
    # Render the page as a PNG image with a resolution of 300 DPI
    pix = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))
    image = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
    return image

if __name__ == '__main__':
    demo, chatbot, show_img, txt, submit_btn, btn = create_demo()
    # Set up event handlers
    with demo:
        # Event handler for uploading a PDF
        btn.upload(render_file, inputs=[btn], outputs=[show_img])

        # Event handler for submitting text and generating response
        submit_btn.click(add_text, inputs=[chatbot, txt], outputs=[chatbot], queue=False).\
            success(generate_response, inputs=[chatbot, txt, btn], outputs=[chatbot,txt]).\
            success(render_file, inputs=[btn], outputs=[show_img])
    demo.launch()
