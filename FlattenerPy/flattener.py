import os
import subprocess
import sys
from open_plus import open_plus as open
import re
import argparse

def is_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file.read(1024)
        return True
    except (UnicodeDecodeError, IOError):
        return False

def get_all_text_files_extensions(root_dir, ignore_directories):
    text_extensions = set()
    ignore_extension = set()
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if any([i_dir in dirpath for i_dir in ignore_directories]):
            continue
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext in text_extensions or not ext or ext in ignore_extension:
                continue
            elif is_text_file(os.path.join(dirpath, filename)):
                text_extensions.add(ext)
            else:
                ignore_extension.add(ext)
    return text_extensions

def get_directory_structure(root_dir):
    try:
        encoding = 'utf-8' if sys.platform != 'win32' else 'cp1252'
        result = subprocess.run(
            ["tree", "/F", root_dir], capture_output=True, text=True, encoding=encoding, shell=True
        )
        return result.stdout
    except FileNotFoundError:
        print("Error: `tree` command is not available.")
        return ""

def flatten(root_dir, output_name, whole_project=True, all_in_one=False, extensions=None, ignore_directories=['.git']):
    if whole_project and extensions:
        raise ValueError(f'The {whole_project=} is set and {extensions} are specified, please choose one')

    if whole_project:
        extensions = get_all_text_files_extensions(root_dir, ignore_directories)

    output_name, _ = os.path.splitext(output_name)
    for extension in extensions:
        extnsn = extension if not all_in_one else ''
        mode = 'w' if not all_in_one else 'a+'

        with open(f'{output_name}{extnsn}', mode, encoding='utf-8') as outfile:
            if not all_in_one:
                outfile.write('"""\nProject Structure\n\n')
                structure = get_directory_structure(root_dir)
                outfile.write(structure)
                outfile.write('\n"""\n\n')
            
            outfile.write("# Combined Code Files\n\n")
            for dirpath, dirnames, filenames in os.walk(root_dir):
                if any([i_dir in dirpath for i_dir in ignore_directories]):
                    continue
                for filename in filenames:
                    if filename.endswith(extension):
                        filepath = os.path.join(dirpath, filename)
                        outfile.write(f"# {'-'*10} Start of {filepath} {'-'*10}\n\n")
                        if is_text_file(filepath) or whole_project:
                            with open(filepath, 'r', encoding='utf-8') as infile:
                                outfile.write(infile.read())
                            outfile.write(f"\n# {'-'*10} End of {filepath} {'-'*10}\n\n")
                        else:
                            raise ValueError(f'The {filepath} is not a text file.')

def inflate(root_dir):
    src_dir = f'{root_dir}/source'
    os.mkdir(src_dir)
    pattern = r'# -{10} Start of .+? -{10}\n.*?# -{10} End of .+? -{10}'
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            os.replace(os.path.join(dirpath, filename), os.path.join(src_dir, filename))

    for filename in os.listdir(src_dir):
        with open(os.path.join(src_dir, filename), 'r', encoding='utf-8') as f:
            raw_text = f.read()
        matches = re.findall(pattern, raw_text, re.DOTALL)
        new_filenames = []
        for match in matches:
            new_filename = re.findall('(?<=# -{10} Start of )(.*?)(?= -{10})', match, re.DOTALL)[0]
            new_filenames.append(new_filename)
        common_prefix = os.path.commonprefix(new_filenames)
        for match in matches:
            new_filename = re.findall('(?<=# -{10} Start of )(.*?)(?= -{10}\n)', match, re.DOTALL)[0].replace(common_prefix, '')
            with open(os.path.join(root_dir, new_filename), 'a+') as f:
                text_without_paths = re.findall(r"# -{10} Start of .+? -{10}\n\n(.*?)(?=# -{10} End of .+? -{10})", match, re.DOTALL)[0]
                f.write(text_without_paths)

def main():
    parser = argparse.ArgumentParser(description="FlattenerPy CLI: A tool to flatten and inflate project folders.")
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Flatten command parser
    flatten_parser = subparsers.add_parser("flatten", help="Flatten a project directory into a single file.")
    flatten_parser.add_argument("root_dir", type=str, help="Path to the project directory to flatten.")
    flatten_parser.add_argument("output_name", type=str, help="Name of the output file.")
    flatten_parser.add_argument(
        "--whole_project", action="store_true", help="Flatten all text files in the project."
    )
    flatten_parser.add_argument(
        "--all_in_one", action="store_true", help="Combine all files into a single output file."
    )
    flatten_parser.add_argument(
        "--extensions", nargs="*", help="List of specific file extensions to flatten, e.g., .py .txt."
    )
    flatten_parser.add_argument(
        "--ignore_directories", nargs="*", default=['.git'], help="Directories to ignore."
    )
    flatten_parser.set_defaults(func=flatten)

    # Inflate command parser
    inflate_parser = subparsers.add_parser("inflate", help="Restore a flattened project file to its original structure.")
    inflate_parser.add_argument("root_dir", type=str, help="Path to the directory to inflate.")
    inflate_parser.set_defaults(func=inflate)

    args = parser.parse_args()
    if args.command == "flatten":
        args.func(args.root_dir, args.output_name, args.whole_project, args.all_in_one, args.extensions, args.ignore_directories)
    elif args.command == "inflate":
        args.func(args.root_dir)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()