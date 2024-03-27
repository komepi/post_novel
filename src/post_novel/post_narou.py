import time
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from narou_data_api.api import Novel,User
from .post import NovelPost
from config import USER, PASSWORD, AGENT_HEADER
class NarouPost(NovelPost):
    top_url="https://syosetu.com"
    login_btn_xpath="/html/body/div[1]/div[1]/div/div[2]/ul/li[3]/a"
    username_name="narouid"
    password_name="pass"
    submit_xpath='/html/body/div[2]/div[1]/div[1]/div/div[1]/form/div[6]/div/input'
    
    user_top_url="https://syosetu.com/user/top/"
    user_element="narouid"
    password_element="pass"
    button_element="mainsubmit"
    login_value="ログイン"
    login_url="https://syosetu.com/login/login/"
    
    def login(self,user,password):
        super(NarouPost,self).login(user,password)
        userid = self.find_element(1,"userid").get_attribute("textContent")
        if userid:
            self.userid=userid
    
    @NovelPost.login_required
    def make_novel(self, title, novels):
        self.user_top()
        self.click_with_update('/html/body/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/a[1]')# 新規作成
        self.send_data(title, "karititle",method=3) #タイトル入力
        self.send_data(novels["honbun"],"novel",method=3)
        self.click_with_update("wrightsubmit",method=1)#新規保存
    
    @NovelPost.login_required
    def next_episode_post(self, ncode, subtitle, novels,dates=None):
        urls = self.get_novel_page(self.userid)
        url = urls[ncode.upper()]
        ziwainput_url = "https://syosetu.com/usernovelmanage/ziwainput/ncode/{}".format(
            url.split("/")[-2]
        )
        print(ziwainput_url)
        #self.driver.get(ziwainput_url)
        self.access_page(ziwainput_url)
        self.driver.save_screenshot("test1.png")
        self.click_with_update("/html/body/div[2]/div[1]/form/div[1]/div[1]/div/label[1]/input")# 直接入力
        self.send_data(novels["honbun"],"/html/body/div[2]/div[1]/form/div[1]/div[1]/div/div[2]/textarea")
        self.send_data(subtitle, "/html/body/div[2]/div[1]/form/div[1]/div[2]/div/input")
        if novels["maegaki"]:
            self.send_data(novels["maegaki"],"/html/body/div[2]/div[1]/form/div[1]/div[4]/div/textarea")
        if novels["atogaki"]:
            self.send_data(novels["atogaki"],"/html/body/div[2]/div[1]/form/div[1]/div[5]/div/textarea")
        if dates:
            self.select_calender(dates)
            self.select_drop(str(int(dates[3].get())),"/html/body/div[2]/div[1]/form/div[1]/div[7]/div/select",0,1)
        self.click_with_update("//*[@id=\"ziwainput\"]") # 次話投稿クリック
        #self.click_with_update("//*[@id=\"ziwainput\"]") # 確認クリック
        
    @NovelPost.login_required
    def get_novel_page(self):
        data = {}
        novel_count = User.get_by_userid(self.userid,of=["nc"]).novel_cnt
        for i in range(novel_count//20+1):
            page=i+1
            r=self.session.get("https://syosetu.com/usernovel/list/?p={}".format(page),headers=AGENT_HEADER)
            html = BeautifulSoup(r.content, "html.parser")
            novel_list=html.find(id="novellist")
            novels_row = novel_list.find_all("tr")

            for i, novel in enumerate(novels_row):
                if i==0:
                    continue
                ncode=novel.find("td",class_="ncode").text
                url = self.top_url+novel.find("td",class_="title").find("a").get("href")
                data[ncode]=url
        return data
        