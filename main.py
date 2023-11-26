# main.py
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from utils.speech import listen, speak
from chatbot.conversation import chat_with_langchain
from chatbot.storage import initialize_pinecone  # Import the Pinecone initialization function

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize LangChain
llm = OpenAI(api_key=openai_api_key)
conversation = ConversationChain(llm=llm, memory=ConversationBufferMemory())

# Initialize Pinecone
pinecone_index = initialize_pinecone()  # Initialize the Pinecone index

def main():
    while True:
        # Listen for user input
        text = listen()
        if text:
            # Generate a response using LangChain's ConversationChain
            response = chat_with_langchain(conversation, text, pinecone_index)
            # Speak the response
            speak(response)

if __name__ == "__main__":
    main()

