import sys
from vertexai.generative_models import Part

from lib import(
    read_file
)
from llms import (
    io_llm
)

def gen_part(func_name: str, func_res: str) -> Part:
    return Part.from_function_response(
        name=func_name,
        response={
            "content": func_res,
        },
    )

input_prompt = ''
if len(sys.argv) < 2:
    # prompt the user to enter an input prompt and wait while he does not
    while True:
        input_prompt = input("Enter an input prompt: ")
        if input_prompt:
            break
else:
    # getting arguments from the command line
    input_prompt = sys.argv[1]

chat_session = io_llm.start_chat()

# prefix the input prompt
tools_prompt = f"""You are a software developer, you have various tools at your disposal.
You will be given an initial query, use these tools, if they are applicable, to answer the query.
If the tools are not applicable, answer the query directly in natural language WITHOUT using the tools.
The query is delimited by dashes.
----------------------------------------
{input_prompt}
----------------------------------------
DO NOT try to look into files that were not explicitly mentioned in the query."""


chat_res = chat_session.send_message(tools_prompt)
function_call_res = None

if hasattr(chat_res, 'candidates') and hasattr(chat_res.candidates[0].content.parts[0], 'function_call'): # type: ignore
    func_call = chat_res.candidates[0].content.parts[0].function_call # type: ignore
    func_name = func_call.name
    func_object = globals().get(func_name)
    if func_object:
        # calling the tools function dynamically with its kwargs if any
        print(f"calling function: {func_name}")
        kwargs = {arg_name: arg_value for arg_name, arg_value in func_call.args.items()}
        function_call_res = func_object(**kwargs)

if function_call_res is None:
    # if the function call did not return a result, we will use the chat response
    print(chat_res.candidates[0].content.text) # type: ignore
    print("operation unsuccessful, exiting...")
    exit(1)

try:
    chat_res = chat_session.send_message(gen_part(func_name, function_call_res))
    print(chat_res.candidates[0].content.text) # type: ignore
except Exception as e:
    print(f"generation failed, try to tell the agent exactly what you want once it has used the tools. Error: {e}")
    exit(1)