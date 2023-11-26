# chatbot/conversation.py
from chatbot.nlp_utils import vectorize_text
from chatbot.nlp_utils import analyze_top_matches
import uuid
import datetime

from chatbot.storage import query_past_conversations

def chat_with_langchain(conversation, user_input, pinecone_index):
    # Check for recall request
    if "do you remember" in user_input:
        # Handle recall request
        response = handle_recall_request(conversation, user_input, pinecone_index)
    else:
        # Regular conversation flow
        response = conversation.run(user_input)
        vector = vectorize_text(user_input + " " + response)
        unique_id = str(uuid.uuid4())

        metadata = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "user_query": user_input,
            "llm_response": response,
        }

        pinecone_index.upsert(vectors=[{'id': unique_id, 'values': vector, 'metadata': metadata}])
    return response

def handle_recall_request(conversation, user_input, pinecone_index):
    # Extracting the topic from the user's recall request
    topic = user_input.replace("do you remember", "").strip()

    # Querying past conversations based on the topic
    results = query_past_conversations(topic, pinecone_index)

    # Check if there are matches from the query
    if results and results['matches']:
        # Analyze top matches to get a combined context
        combined_context = analyze_top_matches(results['matches'])

        # Check if combined context is not None, indicating relevant matches were found
        if combined_context:
            print(combined_context)
            # Create a new prompt with the combined context for the LLM to process
            new_prompt = combined_context + " " + user_input
            return conversation.run(new_prompt)
        else:
            # Fallback response if no relevant matches are found
            return "I don't have enough information about that."
    else:
        # Fallback response if no matches are found
        return "I don't remember that."

def process_recall_results(response):
    # Check if the response contains any matches
    if response['matches']:
        # list of matches
        matches = response['matches']
        print(matches)
        # Assuming the first match is the most relevant
        most_relevant_entry = response['matches'][0]

        # Extracting information from the most relevant entry
        # Assuming the conversation text is stored in metadata
        relevant_text = most_relevant_entry.get('metadata', {}).get('user_query', "I couldn't find that information.")
        return relevant_text
    else:
        return "I couldn't find that information."
