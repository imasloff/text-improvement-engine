from typing import Any


def load_file(path: str) -> Any:
    """
    Loads the file from src directiry, 
    reads and return its contents,
    deals with exceptions.
    """
    try:
        with open(path, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File not found at {path}. Please check the file path.")
        exit(1)
    except Exception as e:
        print(f"Error loading file at {path}: {e}")
        exit(1)


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'csv'}
