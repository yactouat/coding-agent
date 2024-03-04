# gemini coding agent test

## what is this?

An attempt at creating a coding assistant with Gemini.

## How this works

### Pre requisites

- Docker and Docker Compose
- a working Python environment (I use 3.10)
- a GCP project with billing enabled
- Vertex AI API enabled
- a service account with the role `Vertex AI User`
- a JSON key for this service account stored as `vertex-ai-sa.json` in the root of this project (it is in `.gitignore`)

### Entry point

The entry point of the agent is the `y` service in the `docker-compose.yml` file.

Its code is located @ `/src/y.py`.

### Usage

- `cp .env.example .env` and fill in the environment variables
- `docker compose up -d` to start the agent stack (or `docker compose watch` if you are developing the agent)
- `docker compose exec -it y bash` to enter the agent container
- `python y.py "please tell me what you think of this project folder structure"` to talk to the agent

### Features

#### Files I/O

Files I/O is handled via Docker Compose volumes.

The mapped `in` and `out` folders are used to communicate with the agent so it can read and write files.

Writing to files is made programmatically without using LLMs (safer and more practical).

#### Tools

To write code, an agent needs tools, for instance, to write to files, to read from files, to run code, etc.

Function calling allows you to coerce LLMs into giving consistent responses in the form a JSON object. Function calling works by:

- defining function definitions and giving the LLM a prompt
- use the output of the LLM to call a given function
- return the output of the function to the LLM

The process is as follows:

- you write a function definition in `src/func_declarations.py`
- you turn it into a LLM tool in `src/lib.py`

Multiple functions can be added to a tool.

Currently supported tools are:

- `code_writing`: for writing code
- `file_io`: for reading and writing to files (WIP)
