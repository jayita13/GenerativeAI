### Evaluating RAG Systems

The evaluation modules manifest in the following categories:

Faithfulness: Assesses whether the response remains true to the retrieved contexts, ensuring there's no distortion or "hallucination."

Relevancy: Evaluates the relevance of both the retrieved context and the generated answer to the initial query.

Correctness: Determines if the generated answer aligns with the reference answer based on the query (this does require labels).

---------------------------------------------------------------------------------------------------------------------------

Faithfullness Evaluator - Measures if the response from a query engine matches any source nodes. This is useful for measuring if the response was hallucinated.

Relevency Evaluation - Measures if the response + source nodes match the query.

Correctness Evaluator - Evaluates the relevance and correctness of a generated answer against a reference answer.

Retrieval Evaluation - Evaluates the quality of any Retriever module defined in LlamaIndex. use metrics like hit-rate and MRR. These compare retrieved results to ground-truth context for any question. For simpler evaluation dataset creation, we utilize synthetic data generation.

------------------------------------------------------------------------------------------------------------------------------

Reference -> https://docs.llamaindex.ai/en/stable/examples/cookbooks/oreilly_course_cookbooks/Module-3/Evaluating_RAG_Systems/


