
import requests
from .post import NovelPost
from config import USER, PASSWORD, AGENT_HEADER
from bs4 import BeautifulSoup

class KakuyomuPost(NovelPost):
    top_url="https://kakuyomu.jp"
    login_btn_xpath="/html/body/header/div/nav/ul/li[2]/a"
    username_name="email_address"
    password_name="password"
    submit_xpath='/html/body/div/section/form/footer/p[1]/button'
    
    user_top_url="https://kakuyomu.jp/my/works"
    
    user_element = "email_address"
    password_element = "password"
    login_url="https://kakuyomu.jp/login"
    button_element=""
    def get_novel_page(self):
        
        r=self.session.get(self.user_top_url,headers=AGENT_HEADER)
        html = BeautifulSoup(r.content, "html.parser")
        novel_list = html.find_all(class_="worksList-item")
        data = {}
        for novel in novel_list:
            title = novel.find("h2",class_="workColumn-workTitle")
            url = title.find("a").get("href")
            title = title.text
            data[title]=self.top_url+url
        return data
    
    def login_session(self, user, password):
        session = super().login_session(user, password, headers={"X-requested-With":"XMLHttpRequest"})
        return session
    
    @NovelPost.login_required
    def make_novel(self, title, novels):
        pass
    
    @NovelPost.login_required
    def next_episode_post(self):
        pass