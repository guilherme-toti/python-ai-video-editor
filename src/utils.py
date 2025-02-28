import json
import os
from typing import List


def get_file_name(file_path: str) -> str:
    """
    Extract the file name from a given file path.

    Args:
        file_path (str): The full path to the file.

    Returns:
        str: The name of the file without the extension.
    """
    try:
        return os.path.basename(file_path).split(".")[0]
    except Exception as e:
        print(f"Error extracting file name: {e}")
        return file_path


def check_or_create_folder(folder_path: str) -> None:
    """
    Check if a folder exists, and create it if it doesn't.

    Args:
        folder_path (str): The path to the folder to check or create.
    """
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
    except Exception as e:
        print(f"Error creating folder {folder_path}: {e}")


def save_to_file(file_path: str, content: str) -> None:
    """
    Save content to a file.

    Args:
        file_path (str): The path to the file where content will be saved.
        content (str): The content to save in the file.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"Error saving to file {file_path}: {e}")


def read_from_json_file(file_path: str, expected_type=None) -> List:
    """
    Read content from a json file.

    Args:
        file_path (str): The path to the file to read.
        expected_type (type, optional): The expected type of the content. If provided, the content will be cast to this type.

    Returns:
        str: The content of the file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = json.loads(f.read())

        if expected_type is not None and not type(content) == expected_type:
            raise json.decoder.JSONDecodeError("Invalid content format", "", 0)

        return content
