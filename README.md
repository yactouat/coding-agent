# ysistant

## what is this?

My personal coding assistant. With it, you can:

- with an input prompt, have the agent generate a codebase in the `out` folder

## How this works

### Pre requisites

- Docker and Docker Compose
- a working Python environment (I use 3.10)
- a GCP project with billing enabled
- Vertex AI API enabled
- a service account with the role `Vertex AI User`
- a JSON key for this service account stored as `vertex-ai-sa.json` in the root of this project (it is in `.gitignore`)

### Entry point

The entry point of the agent is the `ysistant` service in the `docker-compose.yml` file.

Its code is located @ `/src/ysistant.py`.

### Usage

- `cp .env.example .env` and fill in the environment variables
- `docker compose up -d` to start the agent
- `docker compose exec -it ysistant bash` to enter the container
- `python ysistant.py` to start the agent

### Features

#### Files I/O

Files I/O is handled via Docker Compose volumes.

For now I only support output files for code generation that I map to the `out` folder of this very repo. But you can change that to any folder you like on your machine by changing the `volumes` section of the `ysistant` service in the `docker-compose.yml` file.

(I plan to map an input folder as well in the repo, so that the agent can read code and reflect on existing codebases)

#### Function calling

To write code, an agent needs tools, for instance, to write to files, to read from files, to run code, etc.

Function calling allows you to coerce LLMs into giving consistent responses in the form a JSON object. Function calling works by:

- defining function definitions and giving the LLM a prompt
- use the output of the LLM to call a given function
- return the output of the function to the LLM
