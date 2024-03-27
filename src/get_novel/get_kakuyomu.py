
import requests
from bs4 import BeautifulSoup

from config import AGENT_HEADER

root_url = "https://kakuyomu.jp"
def get_subtitle_url(url):
    r = requests.get(url,headers=AGENT_HEADER)
    html = BeautifulSoup(r.content,"html.parser")
    chps = html.find_all("a",class_=lambda value: value and value.startswith("WorkTocSection_link"))
    titles = html.find_all("div",class_=lambda value: value and value.startswith("WorkTocSection_title"))
    chp_nums = len(chps)
    data = []
    for i in range(chp_nums):
        link = root_url+chps[i].get("href")
        title = titles[i].find("div").find("div").text
        data.append((title,link))
    return data

def get_novel(url):
    r = requests.get(url, headers=AGENT_HEADER)
    html = BeautifulSoup(r.content,"html.parser")
    honbun = html.find("div",class_="widget-episodeBody")
    h_data = []
    honbun_lines = honbun.find_all("p")
    for line in honbun_lines:
        h_data.append(get_line(line))
    
    return "\n".join(h_data)
        
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