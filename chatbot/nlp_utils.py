# chatbot/nlp_utils.py
import os
from sentence_transformers import SentenceTransformer

RELEVANCE_THRESHOLD = float(os.getenv('RELEVANCE_THRESHOLD', 0.5))
SENTENCE_TRANSFORMER_MODEL = os.getenv('SENTENCE_TRANSFORMER_MODEL', 'all-MiniLM-L12-v2')

model = SentenceTransformer('all-MiniLM-L12-v2')



def vectorize_text(text):
    encoded = model.encode(text, convert_to_tensor=False)
    # Convert to list if it's not already
    if not isinstance(encoded, list):
        encoded = encoded.tolist()
    return encoded

def analyze_top_matches(matches):
    # Analyzes the top matches from Pinecone query results.
    combined_context = ""

    # Iterate through each match to build combined context
    for match in matches:
        score = match['score']
        # Filter out matches below the relevance threshold
        if score < RELEVANCE_THRESHOLD:
            continue
        user_query = match['metadata']['user_query']
        llm_response = match['metadata']['llm_response']
        combined_context += f"Q: {user_query} A: {llm_response} "

    # Return combined context if it exists
    return combined_context.strip() if combined_context else None
