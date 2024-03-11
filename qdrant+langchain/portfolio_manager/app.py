from fastapi import FastAPI
import gradio as gr
from gradio_app import demo

app = FastAPI()

@app.get("/")
def read_main():
    return {"message": "This is your main app"}

app = gr.mount_gradio_app(app, demo, path="/gradio")