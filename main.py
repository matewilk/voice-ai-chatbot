# main.py

from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Initialize New Relic
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')
newrelic.agent.register_application(timeout=10)

import os
import signal
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.manager import CallbackManager
from utils.speech import listen, speak
from chatbot.conversation import chat_with_langchain
from chatbot.storage import initialize_pinecone
from nr_openai_observability import monitor
from nr_openai_observability.async_langchain_callback import NewRelicAsyncCallbackHandler
from nr_openai_observability.langchain_callback import NewRelicCallbackHandler

def handler(signum, frame):
    # if user is killing the program, shut down the agent cleanly
    print("flushing New Relic agent")
    newrelic.agent.shutdown_agent(10)
    exit(1)

# catch CTRL-C
signal.signal(signal.SIGINT, handler)

# Get OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize Pinecone
pinecone_index = initialize_pinecone()  # Initialize the Pinecone index

# Wrapper functions
@newrelic.agent.background_task()
@newrelic.agent.function_trace(name="listen")
def listen_wrapper():
    return listen()

@newrelic.agent.background_task()
@newrelic.agent.function_trace(name="chat_with_langchain")
def chat_with_langchain_wrapper(text, pinecone_index):
    # Initialize LangChain
    handlers = [NewRelicCallbackHandler()]
    llm = ChatOpenAI(api_key=openai_api_key, callbacks=CallbackManager(handlers=handlers))
    conversation = ConversationChain(llm=llm, memory=ConversationBufferMemory(), callbacks=CallbackManager(handlers=handlers))

    return chat_with_langchain(conversation, text, pinecone_index)

@newrelic.agent.background_task()
@newrelic.agent.function_trace(name="speak")
def speak_wrapper(response):
    speak(response)

def run_chatbot():
    while True:
        # Listen for user input
        run()
            
# @newrelic.agent.background_task()
# @newrelic.agent.function_trace(name="run")
def run():
        text = listen_wrapper()
        if text:
            # Generate a response using LangChain's ConversationChain
            response = chat_with_langchain_wrapper(text, pinecone_index)
            print(response)
            # Speak the response
            speak_wrapper(response)

def main():
    run_chatbot()

    # shut down the agent cleanly if the listener times out
    newrelic.agent.shutdown_agent(10)


if __name__ == "__main__":
    main()

