# Chatbot setup enviroment

## Macos:
To install the venv:

    python3 -m venv .venv

Then we need to activate the venv:
    source .venv/bin/activate

Then we must install the dependencies:

    pip install fastapi "uvicorn[standard]" pydantic \
    langchain langchain-community langchain-core langchain-text-splitters \
    langchain-huggingface langchain-ollama \
    chromadb sentence-transformers pypdf


Then to reload the app, we do this:

     uvicorn main:app --reload