## Voice-AI Chatbot

### Description
This project implements a voice-activated AI chatbot that uses natural language processing to converse with users and recall past conversations. It leverages LangChain for language model interactions and Pinecone as a vector database for storing and retrieving conversation history.

### Features
- **Voice Interaction**: Engage with the chatbot using voice commands.
- **Conversation Recall**: Ability to recall and reference past conversations.
- **RAG-like System**: Utilizes a Retrieval-Augmented Generation approach for informed response generation.

### Setup
##### Install Dependencies

```bash
pip install -r requirements.txt
```

##### Additional system dependencies
For audio recording and playback, you might need to install the following system dependencies if you don't already have them.

Ubuntu/Debian:

```bash
sudo apt-get install portaudio19-dev
brew install flac
```
MacOS:

```bash
brew install portaudio
brew install flac
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
VOICE_ACCENT=en # Voice accent for answer generation e.g. "en", "fr"
TOP_LEVEL_DOMAIN=co.uk # Top level domain for answer generation e.g. "com", "co.uk"
```

### New Relic (AI observability) Integration 
Make sure  you have your New Relic account and API key ready, if not you can create one [here](https://newrelic.com/signup).
To get your New Relic license key, follow the instructions [here](https://docs.newrelic.com/docs/apis/intro-apis/new-relic-api-keys/).

Generate New Relic configuration file:
```bash
newrelic-admin generate-config {NEW_RELIC_LICENSE_KEY} newrelic.ini
```

Uncomment the following lines in `newrelic.ini`:
```bash
application_logging.enabled = true # Allows us to capture application logs and correlate them with LLM calls
application_logging.forwarding.enabled = true #  Automatically forwards application logs to New Relic (if you have another log forwarding setup, you can use that instead)
distributed_tracing.enabled = true # Enables distributed tracing so that we can understand your application's LLM usage in the context of your overall architecture
```

Add the following lines to `newrelic.ini`:
```bash
custom_insights_events.max_attribute_value = 4095 # Allows us to capture the full text of your LLM calls
event_harvest_config.harvest_limits.ml_event_data = 1000000 # Sets machine learning events per minute to prevent sampling
```

Install New Relic AI observability library (optional as it is already in `requirements.txt`):
```bash
pip install git+https://github.com/newrelic/nr-openai-observability@staging
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
