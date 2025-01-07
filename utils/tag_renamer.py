import argparse

from api.joplinapi import JoplinAPI

"""
Simple tool to rename all tags in the Joplin app.

This will find and replace certain characters with another in the name.

Eg:

gardening:trees

Would become

gardening/trees

This makes use of inline tag plugins that use the / as a separator for parent child tags.
"""


def rename_tag(old_char: str, new_char: str, tag_title: str):
    return tag_title.replace(old_char, new_char)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_url", default="http://127.0.0.1:41184" ,help="The joplin API base URL. Defaults to http://127.0.0.1:41184")
    parser.add_argument("--token", help="The access token for authenticating with the API.")
    parser.add_argument("--old_char", default=":", help="Find all instances of this char in the tag title to be replaced with new char.")
    parser.add_argument("--new_char", default="/", help="All instances of old char will be replaced with new char.")
    args = parser.parse_args()

    api = JoplinAPI(args.base_url, args.token)

    tags = api.get_tags()
    for tag in tags:
        updated_tag_properties = {
            "title": rename_tag(args.old_char, args.new_char, tag["title"]),
        }
        api.update_tag(tag['id'], updated_tag_properties)