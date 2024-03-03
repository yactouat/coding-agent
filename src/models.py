from dotenv import load_dotenv
load_dotenv()

import os
import vertexai
from vertexai.generative_models import (
    GenerativeModel
)

vertexai.init(
    location=os.getenv("VERTEXAI_LOCATION"),
    project=os.getenv("VERTEXAI_PROJECT")
)

gemini_pro = GenerativeModel("gemini-pro")