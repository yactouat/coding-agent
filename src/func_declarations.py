from vertexai.generative_models import FunctionDeclaration, GenerativeModel

read_file_func = FunctionDeclaration(
    name="read_file",
    description="read the contents of a file",
    parameters={
        "type": "object",
        "properties": {"path": {"type": "string", "description": "path to the file"}},
    },
)

write_file_func = FunctionDeclaration(
    name="write_file",
    description="write to a file",
    parameters={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "path to the file"},
            "content": {"type": "string", "description": "content to write"},
        },
    },
)
