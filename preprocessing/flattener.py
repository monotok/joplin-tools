import argparse
import glob
import os
import shutil


"""
This tool will flatten all files in a directory so every file is under a single top level directory. This was used
to explore using Joplin in the zettelkasten style. 

It will copy the files to a new directory. If you wish to use the tagger tool then leave the original export directory
intact.

It currently excludes the Journal and Trilium Demo directory.
"""

def move_files_to_top_level_dir(markdown_directory, output_directory):
    moved_markdown_files = {}
    os.makedirs(output_directory, exist_ok=True)

    for filename in glob.glob(markdown_directory + '/**/*.*', recursive=True):
        old_file_path = os.path.join(os.getcwd(), filename)
        new_file_path = os.path.join(output_directory, os.path.basename(filename))

        if 'Journal' in old_file_path or 'Trilium Demo' in old_file_path:
            continue

        # Copy only files, skip directories
        if os.path.isfile(old_file_path):
            shutil.copy2(old_file_path, new_file_path)  # copy2 preserves metadata
            print(f"Copied {old_file_path} to {new_file_path}")

        moved_markdown_files[filename] = {
            'old_path': old_file_path,
            'new_path': new_file_path,
        }

    return moved_markdown_files

def get_filename_no_path(filename) -> str:
    return os.path.basename(filename)

def get_file_path(filename) -> str:
    return os.path.dirname(filename)


def main(markdown_directory: str, output_directory: str):
    move_files_to_top_level_dir(markdown_directory, output_directory)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown_directory", help="Markdown directory you wish to flatten.")
    parser.add_argument("output_directory", help="The output directory of the flattened markdown files.")
    args = parser.parse_args()
    print(f"Current Working Directory: {os.getcwd()}")
    
    main(args.markdown_directory, args.output_directory)