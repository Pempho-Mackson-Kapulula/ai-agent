import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclarationDict(
    name="run_python_file",
    description="Executes a Python file in a specified working directory with optional additional arguments. Captures stdout, stderr, and exit status.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The base directory in which the Python file resides"
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file relative to the working directory"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional command-line arguments to pass to the Python script"
                ),
                description="Optional list of additional arguments for the Python script"
            )
        },
        required=["working_directory", "file_path"]
    )
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_within_dir = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        is_file = os.path.isfile(target_path)

        if not is_within_dir:
           return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not is_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.lower().endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_path]

        if args:
            command.extend(args)

        
        result = subprocess.run(command, cwd=working_dir_abs,capture_output=True,text=True,timeout=30)
        
        output = []

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        if not result.stdout.strip() and not result.stderr.strip():
            output.append("No output produced")

        if result.stdout.strip():
            output.append(f"STDOUT:\n{result.stdout}")

        if result.stderr.strip():
            output.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output)
                    
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
        

        

