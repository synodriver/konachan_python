# -*- coding: utf-8 -*-
import aiohttp
import aiofiles
from urllib.parse import unquote

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}


def __init__():
    pass


async def download_pic(session: aiohttp.ClientSession, pic_url: str):
    file_name = unquote(pic_url).split("-")[-1]
    async with session.get(pic_url, headers=header) as resp:
        async with aiofiles.open(file_name, "wb") as f:
            await f.write(await resp.read())


async def download_html(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url, headers=header) as response:
        return await response.text()


def main():
    # asyncio.run(get_session())
    pass


if __name__ == "__main__":
    main()
