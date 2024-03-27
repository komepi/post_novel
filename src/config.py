from pathlib import Path
root_path = Path.cwd()
print(root_path)
#CHROME_PATH = root_path.joinpath("..","chromedriver")
CHROME_PATH = "/root/post_novel/src/chromedriver/chromedriver"

AGENT_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
}

MSG_NOT_FOUD_ELEMENT = "要素[%s]は存在しません."

USER="sterben_miyamiya_0921@i.softbank.jp"
PASSWORD="SZzrRVFR3k9BS2FX"