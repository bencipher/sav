CYPHER_TEMPLATE = """
Task:Generate Cypher statement to query a graph database.
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


Example Question 6:
# What did Avatar and Titanic both grossed combined?

Answer:
MATCH (m:Movie)
WHERE m.title IN ["Avatar", "Titanic"]
RETURN m.title AS movie, m.revenue AS revenue
ORDER BY revenue DESC
LIMIT 1 


Note: Do not include any explanations or apologies in your responses.
Use "CONTAINS" for string matching when the name of the movie is more than one words or if it contains franchise of a movie
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

The question is:
{question}"""

AGENT_TEMPLATE = """
You are a movie information assistant. You should only use the knowledge provided to you from 
the tools below or the conversation history. Do not search online or use internal knowledge.

Answer the following questions as best you can. 
Do not search online or use internal knowledge.
You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of Action: [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Previous conversation history:
{history}

Begin!
Question: {input}
Thought: {agent_scratchpad}
"""

GRAPH_HUMAN_MESSAGE = """Based on the following example, extract entities and 
relations from the provided text.\n\n
Ensure that figures are converted to whole numbers or decimals accordingly and the unit is not added to the end of the number.
Use the following entity types, don't use other entity that is not defined below:
# ENTITY TYPES:
{node_labels}

Use the following relation types, don't use other relation that is not defined below:
# RELATION TYPES:
{rel_types}

Below are a number of examples of text and their extracted entities and relationships.
{examples}

For the following text, extract entities and relations as in the provided example.
{format_instructions}\nText: {input}"""

GRAPH_EXAMPLE = [{
    "text": "Oluwafemi was the director of Ellipsis, a film that was released in 2018, "
            "that grossed 1.2m dollars and was a scifi about Africa.",
    "nodes": [
        {
            "id": "Oluwafemi",
            "type": "Person",
            "properties": {
                "name": "Oluwafemi"
            }
        },
        {
            "id": "Ellipsis",
            "type": "Movie",
            "properties": {
                "index": 1,
                "original_title": "Ellipsis",
                "title": "Ellipsis",
                "budget": 0,
                "original_language": "English",
                "overview": "A scifi about Africa",
                "revenue": 1.2e6,
                "status": "Released",
                "vote_average": 0.0,
                "vote_count": 0
            }
        },
        {
            "id": "scifi",
            "type": "Genre",
            "properties": {
                "name": "scifi"
            }
        },
        {
            "id": "Budget_0",
            "type": "Budget",
            "properties": {
                "amount": 0
            }
        },
        {
            "id": "Revenue_1.2e6",
            "type": "Revenue",
            "properties": {
                "amount": 1.2e6
            }
        },
        {
            "id": "English",
            "type": "Language",
            "properties": {
                "name": "English"
            }
        },
        {
            "id": "Released",
            "type": "Status",
            "properties": {
                "name": "Released"
            }
        }
    ],
    "relationships": [
        {
            "source": "Oluwafemi",
            "target": "Ellipsis",
            "type": "DIRECTED",
            "properties": {}
        },
        {
            "source": "Ellipsis",
            "target": "scifi",
            "type": "IN_GENRE",
            "properties": {}
        },
        {
            "source": "Ellipsis",
            "target": "Budget_0",
            "type": "COST",
            "properties": {}
        },
        {
            "source": "Ellipsis",
            "target": "Revenue_1.2e6",
            "type": "GROSSED",
            "properties": {
                "weight": 0.8
            }
        },
        {
            "source": "Ellipsis",
            "target": "English",
            "type": "LANGUAGE_ACTED_IN",
            "properties": {
                "weight": 0.5
            }
        },
        {
            "source": "Ellipsis",
            "target": "Released",
            "type": "CURRENT_STATUS",
            "properties": {
                "weight": 1.0
            }
        }
    ]
},
    {
        "text": "Denis Villeneuve directed The Quantum Enigma, a film released in 2024 with a budget of 200 million dollars, grossing 1.5 billion dollars, and is a sci-fi thriller.",
        "nodes": [
            {
                "id": "Denis Villeneuve",
                "type": "Person",
                "properties": {
                    "name": "Denis Villeneuve"
                }
            },
            {
                "id": "The Quantum Enigma",
                "type": "Movie",
                "properties": {
                    "index": 4,
                    "original_title": "The Quantum Enigma",
                    "title": "The Quantum Enigma",
                    "budget": 200e6,
                    "original_language": "English",
                    "overview": "A sci-fi thriller",
                    "revenue": 1.5e9,
                    "status": "Released",
                    "vote_average": 0.0,
                    "vote_count": 0
                }
            },
            {
                "id": "sci-fi",
                "type": "Genre",
                "properties": {
                    "name": "sci-fi"
                }
            },
            {
                "id": "thriller",
                "type": "Genre",
                "properties": {
                    "name": "thriller"
                }
            },
            {
                "id": "Budget_200e6",
                "type": "Budget",
                "properties": {
                    "amount": 200e6
                }
            },
            {
                "id": "Revenue_1.5e9",
                "type": "Revenue",
                "properties": {
                    "amount": 1.5e9
                }
            },
            {
                "id": "English",
                "type": "Language",
                "properties": {
                    "name": "English"
                }
            },
            {
                "id": "Released",
                "type": "Status",
                "properties": {
                    "name": "Released"
                }
            }
        ],
        "relationships": [
            {
                "source": "Denis Villeneuve",
                "target": "The Quantum Enigma",
                "type": "DIRECTED",
                "properties": {}
            },
            {
                "source": "The Quantum Enigma",
                "target": "sci-fi",
                "type": "IN_GENRE",
                "properties": {}
            },
            {
                "source": "The Quantum Enigma",
                "target": "thriller",
                "type": "IN_GENRE",
                "properties": {}
            },
            {
                "source": "The Quantum Enigma",
                "target": "Budget_200e6",
                "type": "COST",
                "properties": {}
            },
            {
                "source": "The Quantum Enigma",
                "target": "Revenue_1.5e9",
                "type": "GROSSED",
                "properties": {
                    "weight": 0.8
                }
            },
            {
                "source": "The Quantum Enigma",
                "target": "English",
                "type": "LANGUAGE_ACTED_IN",
                "properties": {
                    "weight": 0.5
                }
            },
            {
                "source": "The Quantum Enigma",
                "target": "Released",
                "type": "CURRENT_STATUS",
                "properties": {
                    "weight": 1.0
                }
            }
        ]
    },
    {
        "text": "Patty Jenkins directed The Cyber Detective, a film released in 2024 with a budget of 150 million dollars, grossing 950 million dollars, and is an action mystery.",
        "nodes": [
            {
                "id": "Patty Jenkins",
                "type": "Person",
                "properties": {
                    "name": "Patty Jenkins"
                }
            },
            {
                "id": "The Cyber Detective",
                "type": "Movie",
                "properties": {
                    "index": 5,
                    "original_title": "The Cyber Detective",
                    "title": "The Cyber Detective",
                    "budget": 150e6,
                    "original_language": "English",
                    "overview": "An action mystery",
                    "revenue": 950e6,
                    "status": "Released",
                    "vote_average": 0.0,
                    "vote_count": 0
                }
            },
            {
                "id": "action",
                "type": "Genre",
                "properties": {
                    "name": "action"
                }
            },
            {
                "id": "mystery",
                "type": "Genre",
                "properties": {
                    "name": "mystery"
                }
            },
            {
                "id": "Budget_150e6",
                "type": "Budget",
                "properties": {
                    "amount": 150e6
                }
            },
            {
                "id": "Revenue_950e6",
                "type": "Revenue",
                "properties": {
                    "amount": 950e6
                }
            },
            {
                "id": "English",
                "type": "Language",
                "properties": {
                    "name": "English"
                }
            },
            {
                "id": "Released",
                "type": "Status",
                "properties": {
                    "name": "Released"
                }
            }
        ],
        "relationships": [
            {
                "source": "Patty Jenkins",
                "target": "The Cyber Detective",
                "type": "DIRECTED",
                "properties": {}
            },
            {
                "source": "The Cyber Detective",
                "target": "action",
                "type": "IN_GENRE",
                "properties": {}
            },
            {
                "source": "The Cyber Detective",
                "target": "mystery",
                "type": "IN_GENRE",
                "properties": {}
            },
            {
                "source": "The Cyber Detective",
                "target": "Budget_150e6",
                "type": "COST",
                "properties": {}
            },
            {
                "source": "The Cyber Detective",
                "target": "Revenue_950e6",
                "type": "GROSSED",
                "properties": {
                    "weight": 0.8
                }
            },
            {
                "source": "The Cyber Detective",
                "target": "English",
                "type": "LANGUAGE_ACTED_IN",
                "properties": {
                    "weight": 0.5
                }
            },
            {
                "source": "The Cyber Detective",
                "target": "Released",
                "type": "CURRENT_STATUS",
                "properties": {
                    "weight": 1.0
                }
            }
        ]
    }
]
