from vertexai.generative_models import Tool

from functions import read_file_func

file_io_tool = Tool(
    function_declarations=[read_file_func]
)