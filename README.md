## Voice-AI Chatbot

### Description
This project implements a voice-activated AI chatbot that uses natural language processing to converse with users and recall past conversations. It leverages LangChain for language model interactions and Pinecone as a vector database for storing and retrieving conversation history.

### Features
- **Voice Interaction**: Engage with the chatbot using voice commands.
- **Conversation Recall**: Ability to recall and reference past conversations.
- **RAG-like System**: Utilizes a Retrieval-Augmented Generation approach for informed response generation.

### Setup
##### Install Dependencies:

```basg
pip install -r requirements.txt
```

##### Environment Variables:
Set up `.env` with your API keys and other configurations.
```bash
OPENAI_API_KEY={YOUR_OPENAI_API_KEY}
PINECONE_API_KEY={YOUR_PINECONE_API_KEY}
PINECONE_ENVIRONMENT={YOUR_PINECONE_ENVIRONMENT} # e.g. "us-west1-gcp", "gcp-starter"
PINECONE_INDEX_NAME={YOUR_PINECONE_INDEX_NAME} 
TOKENIZERS_PARALLELISM=false # Set to false to avoid warning
RELEVANCE_THRESHOLD=0.5 # [0, 1]
SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L12-v2 # Sentence transformer model name
VOICE_ACCENT=en-uk # Voice accent for answer generation e.g. "en", "fr"
TOP_LEVEL_DOMAIN=co.uk # Top level domain for answer generation e.g. "com", "co.uk"
```

### Important Notes
- The sentence transformer model `all-MiniLM-L12-v2` used in this project supports 384 dimensions. Ensure your Pinecone index is set up with the same dimension count.
- You can customize the sentence transformer model by setting the environment variable `SENTENCE_TRANSFORMER_MODEL`. The default model is `all-MiniLM-L12-v2`.


### Usage
Run the main script to start interacting with the chatbot:

css
```bash
python3 main.py
```

### Files Description
- `main.py`: The main script to run the chatbot.
- `chatbot/conversation.py`: Handles the conversation logic.
- `chatbot/storage.py`: Manages Pinecone storage interactions.
- `chatbot/nlp_utils.py`: Contains NLP-related utility functions.

### Contributions
Contributions to this project are welcome. Please ensure to follow the project's coding standards and pull request process.

### License
Apache License 2.0
