import requests
from fake_useragent import UserAgent

URL = "https://shikimori.one/api/graphql/"


class Animeapi:

    def __init__(self, title):
        self.title = title
        self.url = URL
        self.headers = {"User-Agent": UserAgent().chrome}

    @property
    def query(self):
        query = f"""{{
        animes(search: "{self.title}", limit: 20, kind: "!special") {{
            id
            name
            score
            russian
            japanese
            status
            episodes
            releasedOn {{ year }}
            poster {{ originalUrl mainUrl }}
            genres {{ name russian kind }}
            studios {{  name  }}
        }}
        }}
        """
        return query

    def fetch_anime_data_by_title(self):
        response = requests.post(
            url=self.url, json={"query": self.query}, headers=self.headers
        )
        return response.json()["data"].get("animes")
