import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclarationDict(
    name="get_file_content",
    description="Reads a file from a specified working directory, returns the first MAX_CHARS characters, truncates if needed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The base directory in which the file resides"
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file relative to the working directory"
            )
        },
        required=["working_directory", "file_path"]
    )
)

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_within_dir = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

        if not is_within_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            # check if file is longer than MAX_CHARS
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content

    except Exception as e:
        return f"ERROR: {e}"