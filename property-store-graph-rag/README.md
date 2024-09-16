References -> https://docs.llamaindex.ai/en/stable/examples/property_graph/property_graph_basic/

Snippet -> https://neo4j.com/blog/what-is-knowledge-graph/

Property Graphs
Native property graph databases, such as Neo4j, are a logical choice for implementing knowledge graphs. They natively store information as nodes, relationships, and properties, allowing for an intuitive visualization of highly interconnected data structures. The physical database matches the conceptual data model, making designing and developing the knowledge graph easier. When you use property graphs, you get:

* Simplicity and ease of design: Property graphs allow for straightforward data modeling when designing the knowledge graph. Because the conceptual and physical models are very similar (often the same), the transition from design to implementation is more straightforward (and easy to explain to non-technical users).

- Flexibility: It’s easy to add new data, properties, relationship types, and organizing principles without extensive refactoring or code rewrites. As needs change, you can iterate and incrementally expand the knowledge graph’s data, relationships, and organization.

- Performance: Property graphs offer superior query performance compared to alternatives like RDF databases or relational databases, especially for complex traversals and many-to-many relationships. This performance comes from storing the relationships between entities directly in the database rather than re-generating them using joins in queries. A native property graph database traverses relationships by following pointers in memory, making queries that traverse even complex chains of many relationships very fast.

- Developer-friendly Code: Property graphs support an intuitive and expressive ISO query language standard, GQL, which means you have less code to write, debug, and maintain than SQL or SPARQL. Neo4j’s Cypher is the most widely used implementation of GQL.

Difference between Triplet Store(RDF) & Property Graph -> https://neo4j.com/blog/rdf-vs-property-graphs-knowledge-graphs/

More in depth -> https://docs.llamaindex.ai/en/latest/module_guides/indexing/lpg_index_guide/
