# spacedev
A LLM trained to use your codebase


# Setup (Docker)

Run with `docker compose up -d <SERVICES...>` where the services placeholder is the services you want to run.

Available services:
- backend
- frontend
- ollama

If you are going to use Ollama, you'll need to pull the models, to do this, run: `docker exec -it ollama ollama pull <MODEL>` where the model placeholder is the model you want to pull, e.g.: `nomic-embed-texts` or `llama3.1`


# Setup

Run the `Setup.ps1` or `setup.sh` script in the root folder to create everything you need to work. You still need to fill .env by yourself, the script just copies it for you.


# How to run

Run the `Start.ps1` or `start.sh` script to start the backend. To use the frontend, enter the frontend folder and run `yarn dev`
