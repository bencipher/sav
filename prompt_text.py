CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Cypher examples:

#Example Questions 1: 
Who directed Pirates of the Carribean?
who was the director of Pirates of the Carribean?
who directed the movie Pirates of the Carribean?
who was the director of the movie Pirates of the Carribean?
Pirates of the Carribean movie was directed by who?
Pirates of the Carribean was directed by who?

Answer:
MATCH (p:Person)-[:DIRECTED]->(m:Movie)
WHERE m.title CONTAINS "Pirates of the Carribean"
RETURN p.name AS director, m.title AS movie

#Example Questions 2: 
Who directed Superman?
who was the director of Superman?
who directed the movie Superman?
who was the director of the movie Superman?
Superman movie was directed by who?
Superman was directed by who?

Answer:
MATCH (p:Person)-[:DIRECTED]->(m:Movie {title: superman})
RETURN p.name AS director, m.title AS movie

#Example Questions 3:
which movies are in English?

Answer:
MATCH (m:Movie)
WHERE m.original_language = "en"
RETURN m.title AS movie

#Example Questions 4:
Which directors directed movies in English, French or Korean?

Answer:
MATCH (p:Person)-[:DIRECTED]->(m:Movie)
WHERE m.original_language IN ["en", "fr", "ko"]
RETURN p.name AS director, m.title AS movie

#Example Questions 5:
What is the top grossing movie?

Answer:
MATCH (m:Movie)
RETURN m.title AS movie, m.revenue AS revenue
ORDER BY revenue DESC
LIMIT 1

Note: Do not include any explanations or apologies in your responses.
Use "CONTAINS" for string matching when the name of the movie is more than one words
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

The question is:
{question}"""