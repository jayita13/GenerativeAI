Reference - https://rito.hashnode.dev/daily-portfolio-summarizer-with-langchain-qdrant-and-mistral-ai

Tweaking -> LLM - GEMINI, Embedding - PALM, DATA - latest

To run application

```
cd portfolio_manager
pip install -r requirements.txt
```

To run streamlit app
```
streamlit run streamlit_app.py
```

To run gradio app -> Uncomment last line ```demo.launch()```
```
python gradio_app.py
```

To run FastAPI mounted with gradio
```
uvicorn app:app --reload
```
