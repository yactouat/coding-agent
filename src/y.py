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
    gen_part,
    generic_llm,
    file_io_llm,
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
func_name, function_call_res, kwargs = return_function_call_res(chat_res)

# now let's ask the refactoring instance to refactor the code
code_prompt = f"""with the input code below, delimited by dashes, output a new version of the code:
- with better performance
- with more comments
- with more features
--------------------------------
{function_call_res}
--------------------------------
Please output syntatically correct Python code without backticks, pre ambles, or any other formatting.
If you want to add comments, add them as regular Python comments."""
code_chat_session = generic_llm.start_chat()
chat_res = code_chat_session.send_message(code_prompt)
new_code = chat_res.candidates[0].content.parts[0].text # type: ignore

# let's write the result in the `out` directory
with open(f"/workspace/out/{file_name}", "w") as file:
    file.write(new_code)