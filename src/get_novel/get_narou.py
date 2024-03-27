from bs4 import BeautifulSoup
import requests
import sys
from config import AGENT_HEADER
root_url = "https://ncode.syosetu.com"
def get_subtitle_url(url):
    """作品ページのURLから各サブタイトルとそのページのURLを取得

    :param url: 作品ページのURL
    :type url: str
    :return: [(サブタイトル, 章ページ),...]
    :rtype: list
    """
    r = requests.get(url,headers=AGENT_HEADER)
    
    html=BeautifulSoup(r.content,"html.parser")
    chp_box = html.find("div", class_="index_box")
    chps = chp_box.find_all("dl", class_="novel_sublist2")
    data = []
    for chp in chps:
        a_tag = chp.find("a")
        subtitle = a_tag.text
        chp_url =  root_url+a_tag.get("href")
        data.append((subtitle,chp_url))
    return data

def get_line(ele):
    """各行を取得.ルビが存在する場合「|テスト《てすと》」の形式で変換

    :param ele: 取得したい行のelement
    :type ele: _type_
    :return: その行の文
    :rtype: _type_
    """
    text=""
    for content in ele.contents:
        if content.name == "ruby":
            rb_text=content.find("rb").get_text()
            rt_text=content.find("rt").get_text()
            text+="|{}《{}》".format(rb_text,rt_text)
        elif content.name == "br":
            text=""
        else:
            text+=content
    return text
def get_novel(url):
    """URLのページの前書き、本文、後書きを取得

    :param url: 取得したい話のURL
    :type url: str
    :return: 前書き, 本文, 後書き
    :rtype: str, str, str
    """
    r = requests.get(url,headers=AGENT_HEADER)
    html=BeautifulSoup(r.content,"html.parser")
    honbun = html.find("div",id="novel_honbun")
    if honbun:
        h_data = []
        honbun_lines = honbun.find_all("p")

        for line in honbun_lines:

            h_data.append(get_line(line))
    
    
    maegaki = html.find("div",id="novel_p")
    p_data = []
    if maegaki:
        maegaki_lines = maegaki.find_all("p")
        
        for line in maegaki_lines:
            p_data.append(get_line(line))
        
    atogaki = html.find("div",id="novel_a")
    a_data=[]
    if atogaki:
        atogaki_lines = atogaki.find_all("p")

        for line in atogaki_lines:
            a_data.append(get_line(line))

    return "\n".join(p_data),"\n".join(h_data),"\n".join(a_data)