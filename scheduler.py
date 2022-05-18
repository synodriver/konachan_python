# -*- coding: utf-8 -*-
import asyncio
import aiohttp
from konachan.downloader import download_html
from konachan.parser import from_url_get_filename, from_html_get_pic, from_html_get_url
from typing import List, Iterable, Tuple
from konachan.database import SQLclient
import time
import sys


start_url: str = "https://konachan.com/post?page={0}&tags="


# start_page: int = 1
def raise_tasks(tasks: Iterable):
    for task in tasks:
        if task.exception():
            raise task.exception()


async def _claw(session: aiohttp.ClientSession, client: SQLclient, page: int):
    print("正在抓取第{0}页".format(page))
    page_url: str = start_url.format(page)
    main_html = await download_html(session, page_url)
    print("主页html下载完成")
    urls = from_html_get_url(main_html)
    # filenames = [from_url_get_filename(url) for url in urls]  # 名字
    if len(urls) != 21:
        print("警告：这一页不是21张可能漏了 {0}".format(page_url))
    # 下载每个分页的html
    tasks = [asyncio.create_task(download_html(session, url)) for url in urls]
    await asyncio.wait(tasks)
    print("分页html下载完成")
    raise_tasks(tasks)
    fenye_html: List[str] = [task.result() for task in tasks]  # 每一个分页的html
    # 分析地址
    pic_urls: List[Tuple[str]] = [from_html_get_pic(i) for i in fenye_html]  # [(name,url),...]
    if len(pic_urls) != 21:
        print("有一个链接没有获取到图片，当前page{0}".format(page_url))
    # 入库
    tasks = [asyncio.create_task(client.insert(url, name, page_url)) for name, url in pic_urls]
    # await client.insert(url, name, page_url)
    await asyncio.wait(tasks)
    raise_tasks(tasks)


async def claw(session: aiohttp.ClientSession, client: SQLclient, page: int, retry: int = None):
    """

    :param session:
    :param client:
    :param page:
    :param retry: None不重试; 0无限重试
    :return:
    """
    if retry is None:
        await _claw(session, client, page)
    elif retry == 0:
        while True:
            try:
                await _claw(session, client, page)
                break
            except aiohttp.ClientConnectionError as e:
                print("连接服务器失败 正在重试")
                print(e.args)
    else:
        while retry > 0:
            try:
                await _claw(session, client, page)
                break
            except aiohttp.ClientConnectionError as e:
                retry -= 1
                print("连接服务器失败 正在重试")
                print(e.args)


async def main():
    client = await SQLclient.create("dbhost", "dbuser", "dbpasswd", 3306, "db")
    async with aiohttp.ClientSession() as session:
        for page in range(11566, 11650):
            await claw(session, client, page)

    await client.close()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        asyncio.set_event_loop(asyncio.ProactorEventLoop())
    star_time = time.time()
    asyncio.run(main())
    print(time.time() - star_time)
