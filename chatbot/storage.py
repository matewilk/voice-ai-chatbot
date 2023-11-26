# chatbot/storage.py
import os
import pinecone

from chatbot.nlp_utils import vectorize_text

def initialize_pinecone():
    # Set up Pinecone API key and environment
    pinecone_api_key = os.getenv('PINECONE_API_KEY')
    pinecone_environment = os.getenv('PINECONE_ENVIRONMENT')
    pinecone_index_name = os.getenv('PINECONE_INDEX_NAME')

        # Ensure environment variables are set
    assert pinecone_api_key is not None, "PINECONE_API_KEY is not set"
    assert pinecone_environment is not None, "PINECONE_ENVIRONMENT is not set"
    assert pinecone_index_name is not None, "PINECONE_INDEX_NAME is not set"

    # Initialize Pinecone
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)

    # Connect to the existing index
    index = pinecone.GRPCIndex(pinecone_index_name)

    return index

def query_past_conversations(query, pinecone_index):
    query_vector = vectorize_text(query)
    results = pinecone_index.query(
        top_k=3,
        include_metadata=True,
        vector=query_vector
    )
    return results
