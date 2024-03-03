from dotenv import load_dotenv
load_dotenv()

import os
import vertexai
from vertexai.generative_models import (
    GenerativeModel
)

from tools import file_io_tool

vertexai.init(
    location=os.getenv("VERTEXAI_LOCATION"),
    project=os.getenv("VERTEXAI_PROJECT")
)

io_llm = GenerativeModel(
    "gemini-pro",
    generation_config={
        "temperature": 0
    },
    tools=[file_io_tool]
)