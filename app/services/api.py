import aiohttp
from fake_useragent import UserAgent
from config import settings


class Animeapi:
    @staticmethod
    def graphql_get_anime_request_format(title):
        return f"""{{
        animes(search: "{title}", limit: 20, kind: "!special") {{
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
        }}"""

    @classmethod
    async def get_anime_by_title(cls, title):
        async with aiohttp.ClientSession() as session:
            headers = {"User-Agent": UserAgent().chrome}
            query = cls.graphql_get_anime_request_format(title)
            response = await session.post(
                settings.API_URL, json={"query": query}, headers=headers
            )
            resp = await response.json()
            return resp["data"].get("animes")
