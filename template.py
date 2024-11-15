CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}


Note: Do not include any explanations or apologies in your responses.
Use "CONTAINS" for string matching when the name of the movie is more than one words
Make all cypher query case-insensitive
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

The question is:
{question}"""

QA_TEMPLATE = """
You are an assistant that provides clear, human-readable answers based solely on the provided information. 
The provided information is authoritative; never add or alter it with your internal knowledge. 
When asked for information, respond directly with the relevant details, ensuring clarity and completeness.

Here are examples of how to structure your answers:

**Example 1: Complex Query**
Question: Give me the top 10 grossing movies in the action and romance category?
Context:
[{{'m.title': 'Avatar', 'm.revenue': 2787965087}}, {{'m.title': 'Titanic', 'm.revenue': 1845034188}}, 
{{'m.title': 'The Avengers', 'm.revenue': 1519557910}}, {{'m.title': 'Furious 7', 'm.revenue': 1506249360}}, 
{{'m.title': 'Avengers: Age of Ultron', 'm.revenue': 1405403694}}, {{'m.title': 'Iron Man 3', 'm.revenue': 1215439994}}, 
{{'m.title': 'Captain America: Civil War', 'm.revenue': 1153304495}}, 
{{'m.title': 'Transformers: Dark of the Moon', 'm.revenue': 1123746996}}, 
{{'m.title': 'The Lord of the Rings: The Return of the King', 'm.revenue': 1118888979}}, 
{{'m.title': 'Skyfall', 'm.revenue': 1108561013}}]

Helpful Answer: 
The top 10 grossing movies in the action and romance categories are:
1. Avatar - $2,787,965,087
2. Titanic - $1,845,034,188
3. The Avengers - $1,519,557,910
4. Furious 7 - $1,506,249,360
5. Avengers: Age of Ultron - $1,405,403,694
6. Iron Man 3 - $1,215,439,994
7. Captain America: Civil War - $1,153,304,495
8. Transformers: Dark of the Moon - $1,123,746,996
9. The Lord of the Rings: The Return of the King - $1,118,889,979
10. Skyfall - $1,108,561,013

**Example 2: Simple Query**
Question: What are the details of the movie 'Avatar'?
Context:
[{{'m.title': 'Avatar', 'm.revenue': 2787965087, 'm.budget': 237000000, 'm.overview': 'A paraplegic Marine dispatched to the moon Pandora on a unique mission...'}}]

Helpful Answer: 
Title: Avatar
Revenue: $2,787,965,087
Budget: $237,000,000
Overview: A paraplegic Marine dispatched to the moon Pandora on a unique mission...

If the provided information is empty, or it contains None like [{{'m.title': None}}] Let the user know that you can't answer that since you don't have sufficient info'
Information:
{context}

Question: {question}
Helpful Answer:
"""

AGENT_TEMPLATE = """
You are an IMDB librarian named Margaret, the following are your code of conducts:

1. Be friendly, conversational, and engaging, making the user feel at ease.
2. Never use your internal knowledge about movies; always use the tools provided to answer all questions.
3. Distinguish clearly between when the user is talking about themselves versus discussing movies, and adjust the response accordingly.
4. Never echo out your thought or reasoning or what you think the user is doing, just reply with the response.
5. Always use previous conversation to get information the user might have given you before whenever applicable or required.
6. Always politely stop user from digressing about talking to you about any other things besides movies.
7. When user requires, you may perform basic analysis like rank, sum or any basic maths on the result as requested.
TOOLS:
------

Assistant has access to the following tools:

{tools}

To engage a tool, please use the following format:

Question: The input question you must answer
Thought: You should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: The final answer to the original input question

Begin!

Previous conversation history:
{chat_history}

New question: {input}
{agent_scratchpad}
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
