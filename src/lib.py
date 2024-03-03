import os

def read_file(*, path: str) -> str | None:
    if not os.path.exists(path):
        return None
    # the asterisk (*) before `path` forces callers to use it as a kwarg.
    try:
        with open(path, "r") as file:
            return file.read()
    except Exception as e:
        return None