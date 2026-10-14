import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Function that writes to a file based on the file path supplied and the context/text inseretd(if a file doesn't exist on the file paht supplied, one will be created)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, relative to current working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "content is how the caller supplies the text to be created in the file",
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        #VERIFY PATHS
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

       #Check/create directory recursively thingy
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error {e}"
