import os

from dotenv import load_dotenv
import requests

load_dotenv()
cl_url = os.getenv("COURTLISTENER_URL")
cl_token = os.getenv("COURTLISTENER_TOKEN")


def search_courtlistener(query: str, page: int = 1, page_size: int = 10) -> list[dict]:
    headers = {}
    if cl_token:
        headers["Authorization"] = f"Token {cl_token}"
    params = {
        "q": query,
        "page": page,
        "page_size": page_size
    }

    response = requests.get(f"{cl_url}/search", headers=headers, params=params)
    response.raise_for_status()
    return response.json()["results"]