"""Tools for the semantic engine to use

"""
import requests


def is_url_live(url):
    try:
        # Add scheme if not present
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        # Send a GET request to the URL
        response = requests.get(url, timeout=5)

        # Check if the status code indicates success (2xx)
        return response.status_code >= 200 and response.status_code < 300
    except requests.RequestException:
        return False
