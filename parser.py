# -*- coding: utf-8 -*-
"""
解析html
"""
from bs4 import BeautifulSoup
from urllib.parse import unquote
from typing import List

prefix = "https://konachan.com"

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}


def __init__():
    pass


def from_url_get_filename(url: str) -> str:
    """
    分页的url
    :param url:
    :return:
    """
    file_name = unquote(url).split("/")[-1]
    return file_name


def from_html_get_pic(html: str) -> List[str]:
    """
    返回图片名字和直连
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, "lxml")
    try:
        pic_url = [tag.attrs["href"] for tag in soup.find_all(name="a", attrs={"class": "original-file-changed"})][0]
    except IndexError:
        pic_url = [tag.attrs["src"] for tag in soup.find_all(name="img", attrs={"class": "image"})][0]
    pic_name = [tag.attrs["alt"] for tag in soup.find_all(name="img", attrs={"class": "image"})][0]
    return pic_name, pic_url
    pass


def from_html_get_url(html: str) -> List[str]:
    """
    从主页面进入分页
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, "lxml")
    return [prefix + tag.attrs["href"] for tag in soup.find_all(name="a", attrs={"class": "thumb"})]


if __name__ == "__main__":
    # with open("test.html", encoding="utf8") as f:
    #     print(len(from_html_get_url(f.read())))
    # with open("neibu.html", encoding="utf8") as f:
    #     print(from_html_get_pic(f.read()))
    # print(from_url_get_filename(
    #     "https://konachan.com/post/show/307794/bang_dream-bikini-breasts-cleavage-hanazono_tae-ic"))
    import requests

    html = requests.get('https://konachan.com/post/show/307852/all_male-animal_ears-bicolored_eyes-brown_hair-cat', headers=header).text

    a=from_html_get_pic(html)
    print(a)
