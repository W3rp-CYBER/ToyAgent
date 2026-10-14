import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        #VERIFY PATHS
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        #Lists directory, file size and is directory
        list_dir = []
        for item in os.listdir(target_dir):
            #Maybe cleaner if I called functions values into variables then use in print ??
            item_abs_path = os.path.join(target_dir, item)
            list_dir.append(f"- {item}: file_size={os.path.getsize(item_abs_path)} bytes, is_dir={os.path.isdir(item_abs_path)}")
        return "\n".join(list_dir)

    except Exception as e:
        return f"Error: {e}"
