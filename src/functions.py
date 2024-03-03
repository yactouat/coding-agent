from vertexai.generative_models import FunctionDeclaration

read_file_func = FunctionDeclaration(
    name="read_file",
    description="read the contents of a file",
    parameters={
        "type": "object",
        "properties": {"path": {"type": "string", "description": "path to the file"}},
    },
)
