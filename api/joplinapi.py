import json

import requests


class JoplinAPI:
    def __init__(self, base_url, token):
        """
        Initialize the JoplinAPI client.

        Args:
            base_url (str): The base URL for the Joplin API (e.g., http://127.0.0.1:41184).
            token (str): The access token for authenticating with the API.
        """
        self.base_url = base_url
        self.token = token

    def get_notes(self, page=1):
        """
        Fetch all notes from the Joplin API.

        Returns:
            list: A list of notes as dictionaries.
        """
        endpoint = f"{self.base_url}/notes"
        params = {"token": self.token, "page": page}
        response = requests.get(endpoint, params=params)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch notes: {response.status_code} - {response.text}")

        json_response = response.json()
        notes = json_response.get('items', [])
        print(f"Fetching page {page}: {len(notes)} notes retrieved.")

        if json_response.get('has_more', False):
            notes += self.get_notes(page=page+1)
        return notes

    def get_tags(self, page=1):
        """
        Fetch all notes from the Joplin API.

        Returns:
            list: A list of notes as dictionaries.
        """
        endpoint = f"{self.base_url}/tags"
        params = {"token": self.token, "page": page}
        response = requests.get(endpoint, params=params)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch tags: {response.status_code} - {response.text}")

        json_response = response.json()
        tags = json_response.get('items', [])
        print(f"Fetching page {page}: {len(tags)} tags retrieved.")

        if json_response.get('has_more', False):
            tags += self.get_tags(page=page+1)
        return tags

    def search(self, query: str, type: str, page=1):
        endpoint = f"{self.base_url}/search"
        params = {"query": query, "type": type, "token": self.token, "page": page}
        response = requests.get(endpoint, params=params)

        if response.status_code != 200:
            raise Exception(f"Failed to search: {response.status_code} - {response.text}")

        json_response = response.json()
        results = json_response.get('items', [])
        print(f"Fetching page {page}: {len(results)} results retrieved.")

        if json_response.get('has_more', False):
            results += self.search(query=query, type=type, page=page+1)
        return results

    def create_tag(self, tag_name: str):
        """
        Create a new tag with the given name.
        :param tag_name:
        :return:
        """
        endpoint = f"{self.base_url}/tags"
        params = {"token": self.token}
        body = {"title": tag_name}
        headers = {"Content-Type": "application/json"}
        response = requests.post(endpoint, params=params, data=json.dumps(body), headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to create tag: {response.status_code} - {response.text}")
        print(f"Created new Tag: {tag_name}")
        return response.json()


    def create_note(self, note_name: str, note_content: str, note_type: str = "markdown"):
        """
        Create a new note with the given name and contents.
        :param tag_name:
        :return:
        """
        endpoint = f"{self.base_url}/notes"
        params = {"token": self.token}
        if note_type == "markdown":
            body = {"title": note_name, "body": note_content}
        elif note_type == "html":
            body = {"title": note_name, "body_html": note_content}
        headers = {"Content-Type": "application/json"}
        response = requests.post(endpoint, params=params, data=json.dumps(body), headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to create note: {response.status_code} - {response.text}")
        print(f"Created new Note: {note_name}")
        return response.json()


    def add_tag_to_note(self, tag_id: str, note_id: str):
        """
        Adds a new tag to the note specified.
        Args:
            tag_name (str): The name of the tag to add.
            note_id (str): The ID of the note to add.
        :return:
        """
        endpoint = f"{self.base_url}/tags/{tag_id}/notes"
        params = {"token": self.token}
        body = {"id": note_id}
        headers = {"Content-Type": "application/json"}
        response = requests.post(endpoint, params=params, data=json.dumps(body), headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to attach tag to note: {response.status_code} - {response.text}")

        return response

    def delete_tag(self, tag_id: str):
        endpoint = f"{self.base_url}/tags/{tag_id}"
        params = {"token": self.token}
        response = requests.delete(endpoint, params=params)

        if response.status_code != 200:
            raise Exception(f"Failed to delete tag: {response.status_code} - {response.text}")
        print(f"Deleted Tag: {tag_id}")
        return response