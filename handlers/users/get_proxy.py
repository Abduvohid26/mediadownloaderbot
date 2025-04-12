from typing import Optional
import httpx
from data.config import GET_TOKEN_URL


async def _get_proxy_url(proxy_token) -> Optional[str]:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(GET_TOKEN_URL, params={"proxy_token": proxy_token})
            print \
                (f"Response: {response.status_code}, {response.text[:100]}...")
            response.raise_for_status()

            data = response.json()
            print(f"Data: {data}")  # Print the entire data for debugging
            return data.get("proxy_url")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
        except httpx.RequestError as e:
            print(f"Request error occurred: {e}")
        except ValueError as e:
            print(f"Error parsing response: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None