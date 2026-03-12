import os
from google.genai import types

schema_write_file = types.FunctionDeclarationDict(
    name="write_file",
    description="Writes the provided content to a file in a specified working directory. Creates missing directories if needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The base directory in which the file should be written"
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the target file relative to the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file"
            )
        },
        required=["working_directory", "file_path", "content"]
    )
)

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_within_dir = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        points_to_dir = os.path.isdir(target_path)

        if not is_within_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if points_to_dir:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"ERROR: {e}"
    
    