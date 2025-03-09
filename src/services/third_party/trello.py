import os
import requests

headers = {"Accept": "application/json"}


class Trello:
    def __init__(self):
        self.base_url = "https://api.trello.com/1"
        self.authentication = {
            "key": os.environ["TRELLO_API_KEY"],
            "token": os.environ["TRELLO_TOKEN"],
        }

    def request(self, url: str, method: str = "GET", query=None):
        """
        Make a request to the Trello API.
        Args:
            url: URL to make the request to
            method: HTTP method to use
            query: Query parameters to include in the request

        Returns:
            requests.Response: Response object from the request
        """
        if query is None:
            query = {}

        params = {**self.authentication, **query}

        response = requests.request(
            method=method,
            url=self.base_url + url,
            headers=headers,
            params=params,
        )

        return response

    def add_comment(self, card_id: str, comment: str):
        """
        Add a comment to a Trello card.
        Args:
            card_id: ID of the card to add the comment to
            comment: Text of the comment to add

        Returns:
            int: Status code of the request
        """
        url = f"/cards/{card_id}/actions/comments"

        query = {"text": comment}

        response = self.request(url=url, method="POST", query=query)

        return response.status_code
