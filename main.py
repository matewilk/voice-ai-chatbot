# main.py

# Initialize New Relic
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')
newrelic.agent.register_application(timeout=10)

import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from utils.speech import listen, speak
from chatbot.conversation import chat_with_langchain
from chatbot.storage import initialize_pinecone
from nr_openai_observability import monitor

# Initialize New Relic OpenAI Observability
monitor.initialization()

# Load environment variables
load_dotenv()

# Get OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize LangChain
llm = OpenAI(api_key=openai_api_key)
conversation = ConversationChain(llm=llm, memory=ConversationBufferMemory())

# Initialize Pinecone
pinecone_index = initialize_pinecone()  # Initialize the Pinecone index

# Wrapper functions
@newrelic.agent.background_task()
def listen_wrapper():
    return listen()

@newrelic.agent.background_task()
def chat_with_langchain_wrapper(conversation, text, pinecone_index):
    return chat_with_langchain(conversation, text, pinecone_index)

@newrelic.agent.background_task()
def speak_wrapper(response):
    speak(response)

def run_chatbot():
    while True:
        # Listen for user input
        text = listen_wrapper()
        if text:
            # Generate a response using LangChain's ConversationChain
            response = chat_with_langchain_wrapper(conversation, text, pinecone_index)
            # Speak the response
            speak_wrapper(response)
            

def main():
    run_chatbot()

if __name__ == "__main__":
    main()

