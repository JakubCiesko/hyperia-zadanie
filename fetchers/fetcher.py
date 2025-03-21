import httpx
import asyncio
import logging

class Fetcher:
    """
    A class for fetching web pages asynchronously using HTTPX.

    Attributes:
        _timeout (int): The request timeout in seconds.
        logger (logging.Logger): Logger instance for error logging.
    """

    def __init__(self, timeout:int=10, logger: logging.Logger = None):
        """
        Initializes the Fetcher with a specified timeout and logger.

        Args:
            timeout (int, optional): The timeout for HTTP requests in seconds. Defaults to 10.
            logger (logging.Logger, optional): A logger instance for error logging. Defaults to None.
        """
        self._timeout = timeout
        self.logger = logger

    def set_timeout(self, timeout:int):
        """
        Sets the timeout value for HTTP requests.

        Args:
            timeout (int): The timeout value in seconds.
        """
        self._timeout = timeout
    
    def get_timeout(self) -> int:
        """
        Retrieves the current timeout setting.

        Returns:
            int: The timeout value in seconds.
        """
        return self._timeout

    async def fetch(self, url: str) -> str:
        """
        Fetches the HTML content of a given URL asynchronously.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the fetched URL, or an empty string if an error occurs.
        """
        async with  httpx.AsyncClient(timeout=self.get_timeout()) as client: 
            return await self._fetch_single(client, url)

    async def fetch_many(self, *urls) -> dict[str, str]:
        """
        Fetches multiple URLs asynchronously.

        Args:
            *urls (str): A variable number of URLs to fetch.

        Returns:
            dict[str, str]: A dictionary mapping URLs to their fetched HTML content.
        """
        async with httpx.AsyncClient(timeout=self.get_timeout()) as client:
            tasks = [self._fetch_single(client, url) for url in urls]
            results = await asyncio.gather(*tasks)
            return {url: result for url, result in zip(urls, results)}
    
    async def _fetch_single(self, client: httpx.AsyncClient, url: str) -> str:
        """
        Performs an individual HTTP GET request.

        Args:
            client (httpx.AsyncClient): The HTTPX client instance.
            url (str): The URL to fetch.

        Returns:
            str: The response text if successful, or an empty string if an error occurs.
        """
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error fetching {url}: {e}")
        except httpx.RequestError as e:
            self.logger.error(f"Request error fetching {url}: {e}")
        return ""
