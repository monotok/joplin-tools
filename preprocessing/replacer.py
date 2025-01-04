import argparse
import glob
import os
import re

"""
This tool fixes the issues with Joplin not importing images with spaces in the name. This has been tested with an
export from Trilium notes application.

It will rename the image files (or any file with the matching extension).
Then it will look for the file references in the markdown files and update them with the new name.
"""


REGEX_FILE_SPACES = "!\\[[^\\]]*\\]\\(([^)]*\\s[^)]*)\\)"

def replace_file_spaces_markdown(markdown_directory, found_images):
    replaced_images = []

    for filename in glob.glob(markdown_directory + '/**/*.md', recursive=True):
        file_path = os.path.join(os.getcwd(), filename)

        with open(file_path, 'r') as f:
            content = f.readlines()  # Read the whole file as a list of lines

        # Process the content and replace image paths
        for i, line in enumerate(content):
            found_image = re.search(REGEX_FILE_SPACES, line)
            if found_image:
                original_filename = next((key for key, value in found_images.items() if key == found_image.group(1)), None)
                if original_filename:
                    # Replace the old path with the new one
                    line = line.replace(original_filename, found_images[original_filename])
                    print(f"Replaced {original_filename} with {found_images[original_filename]}")
                    replaced_images.append(original_filename)
                    content[i] = line  # Update the line with the replaced value

        # Write the modified content back to the same file
        with open(file_path, 'w') as f:
            f.writelines(content)

    return replaced_images


def get_filename_no_path(filename) -> str:
    return os.path.basename(filename)

def get_file_path(filename) -> str:
    return os.path.dirname(filename)

def rename_image_files(image_mapping):
    for old_path, new_path in image_mapping.items():
        # Ensure the directory structure remains the same
        old_abs_path = os.path.abspath(old_path)
        new_abs_path = os.path.abspath(new_path)

        # Get the directory and validate paths
        old_dir = os.path.dirname(old_abs_path)
        new_dir = os.path.dirname(new_abs_path)
        if old_dir != new_dir:
            print(f"Skipping {old_abs_path}: new path must be in the same directory")
            continue

        # Rename the file
        try:
            os.rename(old_abs_path, new_abs_path)
            print(f"Renamed: {old_abs_path} -> {new_abs_path}")
        except FileNotFoundError:
            print(f"File not found: {old_abs_path}")
        except PermissionError:
            print(f"Permission denied: {old_abs_path}")
        except Exception as e:
            print(f"Failed to rename {old_abs_path} -> {new_abs_path}: {e}")

def find_all_files_with_spaces(markdown_directory: str, file_types: list):
    found_images = {}
    for file_type in file_types:
        for filename in glob.glob(markdown_directory + '/**/*.' + file_type, recursive=True):
            if get_filename_no_path(filename).find(' ') != -1:
                new_filename = get_filename_no_path(filename).replace(' ', '_')
                new_filename_and_path = get_file_path(filename)+'/'+new_filename
                rename_image_files({filename: new_filename_and_path})
                filename_no_path = get_filename_no_path(filename)
                found_images[filename_no_path] = filename_no_path.replace(' ', '_')
    return found_images


def main(markdown_directory: str, file_types: list):
    found_files = find_all_files_with_spaces(markdown_directory, file_types)  # Get the mapping of images with spaces
    print(f"Found {len(found_files)} files with spaces in their markdown directory.")
    replaced_files = replace_file_spaces_markdown(markdown_directory, found_files)  # Replace occurrences
    print(f"Replaced images: {replaced_files}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown_directory", help="Markdown directory containing references to images with spaces in the title.")
    parser.add_argument("--file_types", nargs='?', default='jpg jpeg png', help="File types to replace.")
    args = parser.parse_args()
    print(f"Current Working Directory: {os.getcwd()}")

    list_file_types = args.file_types.split(' ')
    main(args.markdown_directory, list_file_types)