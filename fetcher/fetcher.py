import httpx
import asyncio

class Fetcher:
    def __init__(self, timeout:int=10):
        self.timeout = timeout

    async def fetch(self, url: str) -> str:
        async with  httpx.AsyncClient(timeout=self.timeout) as client: 
            return await self._fetch_single(client, url)

    async def fetch_many(self, *urls) -> dict[str, str]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            tasks = [self._fetch_single(client, url) for url in urls]
            results = await asyncio.gather(*tasks)
            return {url: result for url, result in zip(urls, results)}
    
    async def _fetch_single(self, client: httpx.AsyncClient, url: str) -> str: 
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            print(f"{e}")
        except httpx.RequestError as e:
            print(f"{e}")
        return ""
