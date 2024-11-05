# FlatterenrPy

FlatterenrPy is a Python module designed to facilitate flattening and inflating directory structures. It combines text files from a directory into a single output file, preserving directory structure within comments, and can then reconstruct the original files from this combined format.

## Features

- **Flatten**: Combines files with specific extensions or all files into one or multiple output files.
- **Inflate**: Recreates the original files from a combined output, preserving file content and structure.
- **Directory Structure**: Uses the `tree` command to get a visual representation of the directory structure.
- **File Type Detection**: Only includes text files based on encoding detection.

## Installation

To use FlatterenrPy, clone the repository and install the dependencies.

```bash
python -m pip install FlattenerPy
```

## Usage

### Functions

1. **`flatten(root_dir, output_name, whole_project=True, all_in_one=False, extensions=[], ignore_directories=['.git'])`**

   - Combines text files from a directory.
   - **Parameters**:
     - `root_dir`: Root directory to flatten.
     - `output_name`: Base name of the output file/files.
     - `whole_project`: If `True`, flattens the entire project; ignores `extensions`.
     - `all_in_one`: If `True`, combines everything into a single file.
     - `extensions`: List of file extensions to include (ignored if `whole_project=True`).
     - `ignore_directories`: List of directories to ignore.
   - **Returns**: None

   - **Example**:
     ```python
     flatten('/path/to/project', 'output_file.txt', whole_project=True, all_in_one=True)
     ```

2. **`inflate(root_dir)`**

   - Recreates the original directory structure from a flattened output.
   - **Parameters**:
     - `root_dir`: Directory where files will be inflated.
   - **Returns**: None

   - **Example**:
     ```python
     inflate('/path/to/output')
     ```

3. **`get_all_text_files_extensions(root_dir, ignore_directories)`**

   - Returns a set of file extensions for all text files within the directory.
   - **Parameters**:
     - `root_dir`: Root directory to scan.
     - `ignore_directories`: List of directories to ignore.

4. **`get_directory_structure(root_dir)`**

   - Gets the directory structure using the `tree` command.
   - **Parameters**:
     - `root_dir`: Root directory.
   - **Returns**: Directory structure as a string.

5. **`is_text_file(file_path)`**

   - Checks if a file is a text file based on encoding.

### Examples

#### Flattening an Entire Project

```python
from FlatterenrPy import flatten

flatten('/path/to/project', 'output_file.txt', whole_project=True, all_in_one=True)
```

#### Flattening with Specific Extensions

```python
from FlatterenrPy import flatten

flatten('/path/to/project', 'output_file.txt', whole_project=False, extensions=['.py', '.md'])
```

#### Inflating a Flattened File

```python
from FlatterenrPy import inflate

inflate('/path/to/inflated_output')
```

## Requirements

- `tree` command (for directory structure on non-Windows systems).
- Python 3.6+

## License

This project is licensed under the MIT License.