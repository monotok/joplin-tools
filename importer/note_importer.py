import argparse
import glob
import os

from api.joplinapi import JoplinAPI

"""
This will create notes using the Joplin API. It can do this for both markdown and other text based files.

This was used to import non markdown files such as .xml .c .h .css etc that the standard Joplin import tool in the
application ignores.
I had these files because Trilium can create different files, eg source code files and then it exports them as such.

This will import these into Joplin and will wrap them in a code block unless its a markdown file.
"""

def get_filename_no_path(filename) -> str:
    return os.path.basename(filename)


def create_notes(markdown_directory: str, file_type: str, api: JoplinAPI):
    for filename in glob.glob(markdown_directory + '/**/*.' + file_type, recursive=True):
        file_path = os.path.join(os.getcwd(), filename)

        with open(file_path, 'r') as f:
            content = f.read()
        if file_type == 'md':
            api.create_note(get_filename_no_path(filename), content)
        elif file_type == 'html':
            api.create_note(get_filename_no_path(filename), content, note_type='html')
        else:
            api.create_note(get_filename_no_path(filename), f"```{content}```")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown_directory", help="Markdown directory that you want to import notes from.")
    parser.add_argument("--base_url", default="http://127.0.0.1:41184" ,help="The joplin API base URL. Defaults to http://127.0.0.1:41184")
    parser.add_argument("--token", help="The access token for authenticating with the API.")
    parser.add_argument("--file_types", nargs='?', default='md', help="File types to import notes from. Defaults to 'md'. Multiple files can be passed separated by a space.")
    args = parser.parse_args()

    file_types = args.file_types.split(' ')

    api = JoplinAPI(args.base_url, args.token)

    for file_type in file_types:
        create_notes(args.markdown_directory, file_type, api)
