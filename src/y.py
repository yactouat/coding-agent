from dotenv import load_dotenv
load_dotenv()

import os
import sys
import vertexai

vertexai.init(
    location=os.getenv("VERTEXAI_LOCATION"),
    project=os.getenv("VERTEXAI_PROJECT")
)

from lib import (
    file_io_llm,
    code_writing_llm,
    return_function_call_res
)

# preparing the input prompt
if len(sys.argv) >= 2:
    file_name = sys.argv[1]
else:
    while True:
        file_name = input("Please enter the file name: ")
        if file_name:
            break
read_file_prompt = f'read the code in file {file_name}'

# start the files I/O chat session
files_chat_session = file_io_llm.start_chat()

# let Gemini dedicated to files I/O read the file
# TODO replace with a lesser model like `chat-bison002`
chat_res = files_chat_session.send_message(read_file_prompt)
func_name, function_call_res = return_function_call_res(chat_res)

# now let's ask the refactoring instance to refactor the code
code_prompt = f"""with the input code below, delimited by dashes, output a new version of the code:
- with more features
- with better performance
- with more comments
--------------------------------
{function_call_res}
--------------------------------
It's okay if you don't manage to either add features, improve performance or add comments; just output a new version of the code.
"""
code_chat_session = code_writing_llm.start_chat()
chat_res = code_chat_session.send_message(code_prompt)
func_name, function_call_res = return_function_call_res(chat_res)

print(function_call_res)
