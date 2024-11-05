import os

def open_plus(filepath, mode='r', *args, **kwargs):
    # Check if mode includes '+' for write/update mode
    if '+' in mode or 'w' in mode or 'a' in mode:
        # Extract directory from the filepath
        dir_name = os.path.dirname(filepath)
        # If there is a directory path, ensure it exists
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
    
    # Use the built-in open function with the provided arguments
    return open(filepath, mode, *args, **kwargs)
