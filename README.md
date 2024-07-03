
# Project: Movie Knowledge Graph RAG Chat

## Overview

This project is a comprehensive solution for interacting with a movie knowledge graph using natural language queries. The system leverages a combination of tools, including Neo4j for graph databases, LangChain for language models, and Streamlit for the web interface. It is designed to enable users to query a knowledge graph about movies, retrieve relevant information, and save new information into the graph.

## Features

1. **Interactive Chat Interface**: The project provides an interactive chat interface using Streamlit where users can ask questions about movies.
2. **Knowledge Graph Integration**: Uses Neo4j to store and query movie information.
3. **Natural Language Processing**: Utilizes LangChain and Google Generative AI to understand and process natural language queries.
4. **Memory Management**: Maintains conversation context using LangChain's ConversationBufferWindowMemory.
5. **Custom Tools**: Implements custom tools for saving new movie information and searching for movie information.
6. **Embeddings and Vector Store**: Uses HuggingFace embeddings and Pinecone vector store for advanced querying capabilities.
7. **Setup Scripts**: Provides setup scripts to initialize the knowledge graph and vector store with movie data.

## Project Structure

\`\`\`plaintext
.
├── main.py
├── setup.py
├── vector.py
├── parser.py
├── tools.py
├── graph_lib.py
├── custom_prompts.py
├── prompt_text.py
├── config.py
├── cypher_text.py
├── requirements.txt
└── utils.py
\`\`\`

## Setup Instructions

### Prerequisites

1. Python 3.11 or higher
2. Neo4j Cloud Database Account
3. Pinecone API
4. Streamlit
5. Environment variables set in a \`.env\` file

### Environment Variables

Create a \`.env\` file in the root directory of your project and add the following variables:

\`\`\`env
NEO4J_URI=your_neo4j_uri
NEO4J_USERNAME=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password
PINECONE_API_KEY=your_pinecone_api_key
STAGE=your_stage
DATA_PATH=path_to_your_data_file
\`\`\`

### Installation

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/bencipher/sav.git
   cd movie-knowledge-graph-chat
   \`\`\`

2. Install the required dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

### Initial Setup

1. **Setup Knowledge Graph**

   Run the \`setup.py\` script to initialize the knowledge graph with movie data:

   \`\`\`bash
   python setup.py
   \`\`\`

   This script will:
   - Read movie data from the specified file.
   - Setup the graph schema.
   - Write data to the Neo4j graph.

2. **Setup Vector Store**

   (Optional) Uncomment the \`setup_vector_store\` call in \`setup.py\` and run it to initialize the Pinecone vector store with embeddings:

   \`\`\`python
   if __name__ == "__main__":
       setup_graph_kb()
       setup_vector_store()  # Uncomment this line
   \`\`\`

   \`\`\`bash
   python setup.py
   \`\`\`

### Running the Application

Start the Streamlit application:

\`\`\`bash
streamlit run main.py
\`\`\`

This will launch a web interface where you can interact with the movie knowledge graph by typing queries and receiving responses.

## Detailed Explanation of Modules

### \`main.py\`

The main entry point of the application. Sets up the chat interface using Streamlit and handles user interactions. It initializes the language model, tools, prompt templates, and agents required for processing queries.

### \`setup.py\`

Contains the setup logic for initializing the knowledge graph and vector store. Reads movie data from a CSV file, sets up the graph schema, and writes data to the Neo4j database.

### \`vector.py\`

Handles the creation and management of the Pinecone vector store. Includes functions to create an index, generate embeddings, and query the vector store for movie information.

### \`parser.py\`

Defines a custom output parser to handle the responses from the language model. Parses the output to determine the appropriate actions or final answers.

### \`tools.py\`

Implements custom tools for interacting with the knowledge graph. Includes functions for searching movie information and saving new information into the graph.

### \`graph_lib.py\`

Contains utility functions for interacting with the Neo4j graph database. Includes functions to query the knowledge graph, create nodes and relationships, and write data to the graph.

### \`custom_prompts.py\`

Defines custom prompt templates for generating queries to the language model. Utilized by the agent to structure the prompts based on user input and intermediate steps.

### \`prompt_text.py\`

Stores the text templates used in the prompts for the language model. These templates guide the language model in generating appropriate responses.

### \`config.py\` and \`cypher_text.py\`

Contains configuration settings and Cypher query templates used for interacting with the Neo4j database.

### \`requirements.txt\`

Lists all the dependencies required to run the project. Ensures that the correct versions of packages are installed.

### \`utils.py\`

Contains miscellaneous utility functions used throughout the project.

## Conclusion

This project provides a simple RAG for interacting with a movie knowledge graph using natural language queries. By following the setup instructions, you can initialize the system with movie data and start querying the knowledge graph through an interactive chat interface. The modular design and comprehensive feature set make it a robust solution for movie information retrieval and management.
