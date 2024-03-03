import os
from vertexai.generative_models import (
    GenerativeModel,
    Part,
    Tool
)

from func_declarations import (
    read_file_func,
    write_code_func,
    write_file_func
)

code_writing_tool = Tool(
    function_declarations=[
        write_code_func
    ]
)
code_writing_llm = GenerativeModel(
    # "chat-bison-32k@002",
    "gemini-pro",
    tools=[code_writing_tool]
)

file_io_tool = Tool(
    function_declarations=[
        read_file_func,
        write_file_func
    ]
)

file_io_llm = GenerativeModel(
    "gemini-pro",
    generation_config={"temperature": 0},
    tools=[file_io_tool]
)

def gen_part(func_name: str, func_res: str) -> Part:
    return Part.from_function_response(
        name=func_name,
        response={
            "content": func_res,
        },
    )

def read_file(*, path: str) -> str | None:
    if not os.path.exists(path):
        return None
    # the asterisk (*) before `path` forces callers to use it as a kwarg.
    try:
        with open(path, "r") as file:
            return file.read()
    except Exception as e:
        return None
    
def write_code(*, code: str) -> str | None:
    chat = code_writing_llm.start_chat()
    chat_res = chat.send_message(f"""You are a software developer.
With the code below, delimited by dashes, refactor to make it more efficient.
Do not hesitate to the features that you see fit to the existing code.
--------------------------------
{code}""")
    try:
        return chat_res.candidates[0].content.parts[0].text # type: ignore
    except Exception as e:
        return None
    
def write_file(*, path: str, content: str) -> str | None:
    if not os.path.exists(path):
        return None
    try:
        with open(path, "a") as file:
            file.write('\n\n# ---SO GENERATED CONTENT---\n\n')
            file.write(content)
            file.write('\n\n# ---EO GENERATED CONTENT---\n\n')
            return content
    except Exception as e:
        return None

def return_function_call_res(chat_res):
    func_name = None
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
            print(f"function call result: {function_call_res}")
    return func_name, function_call_res