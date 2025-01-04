import argparse

from api.joplinapi import JoplinAPI

"""
Simple tool to delete all tags in the Joplin app.

Even deleting tags still leaves them behind if you do a api call to list them.
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_url", default="http://127.0.0.1:41184" ,help="The joplin API base URL. Defaults to http://127.0.0.1:41184")
    parser.add_argument("--token", help="The access token for authenticating with the API.")
    args = parser.parse_args()

    api = JoplinAPI(args.base_url, args.token)

    tags = api.get_tags()
    for tag in tags:
        api.delete_tag(tag['id'])