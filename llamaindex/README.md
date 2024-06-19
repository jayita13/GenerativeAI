RAG use-case implementation using Llamaindex

[Updated Colab notebook with Llama3](https://colab.research.google.com/drive/10A9OeLQUQyHXf4KciA-VfWwa9Unv9nh9?usp=sharing)

Supercharge your RAG pipeline with the following:

- Framework -> [Llamaindex](https://docs.llamaindex.ai/en/stable/index.html) 
- Loader -> [SimpleDirectoryLoader](https://docs.llamaindex.ai/en/stable/module_guides/loading/simpledirectoryreader.html)
- Chunking -> [Semantic Chunking](https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_chunking.html)
- Embeddings -> [Gemini Embeddings](https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_chunking.html)
- Vector DB -> [Llamaindex VectorStoreIndex](https://docs.llamaindex.ai/en/stable/module_guides/indexing/vector_store_index.html)
- LLM -> [Groq Mistral](https://docs.llamaindex.ai/en/stable/examples/llm/groq.html#groq)
- Reranking -> [Cohere Rerank Model](https://docs.llamaindex.ai/en/stable/examples/node_postprocessor/CohereRerank.html)

For index creation follow notebook file ```rag.ipynb```

To run application:

``` 
pip install -r requirements.txt 
chainlit run app.py 
```

[Follow-up Medium blog/article](https://itsjb13.medium.com/building-a-rag-chatbot-using-llamaindex-groq-with-llama3-chainlit-b1709f770f55)

[Hosted Huggingface App on Spaces](https://huggingface.co/spaces/itsJB/Finance_Knowledge_Bot)
