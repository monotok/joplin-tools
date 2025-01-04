import argparse
import glob
import os
import sys

from api.joplinapi import JoplinAPI

"""
Trilium was more hierarchical in nature and therefore the exported directory structure was very nested. When it was flattened
using the flatten tool, the notes lost all of their context.

Therefore this is a crude tagging tool that looks at the original export directory (after the replacer has been run)
and builds a list of tags which is just the parent directories of the note excluding the base directory.

For example.

/home/me/notes/export/tech/linux/ubuntu/apt proxy.md

This will get these tags:

- linux
- ubuntu

It will search for the corresponding note in Joplin (using name excluding the extension unless its a markdown file) and
update the tags of the note.
"""

def calculate_tags_for_files(markdown_directory, file_extensions: [], tag_prefix: str = "tech:"):
    markdown_tags = {}
    for file_extension in file_extensions:
        for filename in glob.glob(markdown_directory + '/**/*.' + file_extension, recursive=True):
            file_path = os.path.join(os.getcwd(), filename)

            if 'Journal' in file_path:
                continue

            # Copy only files, skip directories
            if os.path.isfile(file_path):
                relative_path = os.path.relpath(file_path, markdown_directory)
                relative_path = str.lower(relative_path)
                markdown_tags[get_filename(filename)] = {
                    'tags': [f"{tag_prefix}{tag.rstrip()}" for tag in os.path.dirname(relative_path).split(os.sep)],
                }

    return markdown_tags

def get_filename(filename) -> str:
    """
    Will return the filename without the extension if a markdown file.
    Any other file extension will keep the extension as the notes will have been imported
    with the extension as part of the note name. See note importer.
    :param filename:
    :return:
    """
    if filename.endswith('.md'):
        return os.path.basename(filename).split('.')[0]
    else:
        return os.path.basename(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown_directory", help="Markdown directory that you want to process tags from. Will use the directory tree of each note to determine tags. Notes name must match name in Joplin.")
    parser.add_argument("--base_url", default="http://127.0.0.1:41184" ,help="The joplin API base URL. Defaults to http://127.0.0.1:41184")
    parser.add_argument("--token", help="The access token for authenticating with the API.")
    parser.add_argument("--file_types", nargs='?', default='md', help="File types to process tags from. Defaults to 'md'. Multiple files can be passed separated by a space.")
    args = parser.parse_args()

    file_types = args.file_types.split(' ')

    api = JoplinAPI(args.base_url, args.token)

    notes_tags = calculate_tags_for_files(args.markdown_directory, file_types)

    notes = api.get_notes()
    for note in notes:
        if note['title'] in notes_tags:
            print(f"Found Note: Title: {note['title']}, ID: {note['id']}")
            for tag in notes_tags[note['title']]['tags']:
                if tag == "":
                    continue
                found_tags = api.search(query=tag, type='tag')
                if len(found_tags) > 1:
                    print(f"Found multiple tags for this search {tag}.")
                    sys.exit(1)
                if not found_tags:
                    print(f"No tags found for this search {tag}.")
                    tag_id = api.create_tag(tag)
                    existing_tags = api.get_tags()
                else:
                    tag_id = found_tags[0]['id']
                try:
                    api.add_tag_to_note(tag_id, note['id'])
                    print(f"Added {tag} to Note: {note['title']}")
                except Exception as e:
                    print(f"Failed to add {tag} to Note: {note['title']}")
                    print(e)
