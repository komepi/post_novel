from post_novel.post_narou import NarouPost
from post_novel.post_kakuyomu import KakuyomuPost
from get_novel.get_narou import get_novel,get_subtitle_url
from get_novel.get_kakuyomu import get_subtitle_url as get_subtitle_url_kakuyomu
from get_novel.get_kakuyomu import get_novel as get_novel_kakuyomu
from narou_data_api.api import User
if __name__=="__main__":
    
    #np=NarouPost()
    #np.login("sterben_miyamiya_0921@i.softbank.jp","SZzrRVFR3k9BS2FX")
    #data=np.get_novel_page()
    #print(data)
    #
    #titles = get_subtitle_url("https://ncode.syosetu.com/n0919ga/")
    #print(titles)
    #
    #mae,hon,ato=get_novel(url=titles[0][1])
#   

    #kp = KakuyomuPost()
    #kp.login("sterben_miyamiya_0921@i.softbank.jp","kyousuke957445")
    #data = kp.get_novel_page()
    #print(data)
    
    titles = get_subtitle_url_kakuyomu("https://kakuyomu.jp/works/1177354054890224894")
    print(titles)
    hon=get_novel_kakuyomu(titles[0][1])
    print(hon)
    #from selenium import webdriver
    #from selenium.webdriver.chrome.service import Service
    #from selenium.webdriver.support.ui import WebDriverWait
    #from selenium.webdriver.support import expected_conditions as EC
    #from selenium.webdriver.common.by import By
    #options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    #options.add_argument('--no-sandbox')
    #options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.1234.56 Safari/537.36')
    #service = Service(executable_path="/root/post_novel/src/chromedriver-linux64/chromedriver")
    #driver=webdriver.Chrome(service=service,options=options)
    #driver.get("https://kakuyomu.jp/")
    #WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "globalHeaderPC-logo")))
    #driver.save_screenshot("test.png")
    #print(driver.page_source)
    