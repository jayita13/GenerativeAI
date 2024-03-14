RAG use-case implementation using Llamaindex

Supercharge your RAG pipeline with the following:

- Framework -> [Llamaindex](https://docs.llamaindex.ai/en/stable/index.html) 
- Loader -> [SimpleDirectoryLoader](https://docs.llamaindex.ai/en/stable/module_guides/loading/simpledirectoryreader.html)
- Chunking -> [Semantic Chunking](https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_chunking.html)
- Embeddings -> [Gemini Embeddings](https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_chunking.html)
- Reranking -> [Cohere Rerank Model](https://docs.llamaindex.ai/en/stable/examples/node_postprocessor/CohereRerank.html)
- LLM -> [Groq Mistral](https://docs.llamaindex.ai/en/stable/examples/llm/groq.html#groq)

For index creation follow notebook file ```rag.ipynb```

To run application:

``` 
pip install -r requirements.txt 
chainlit run app.py 
```
