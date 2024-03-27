
import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from config import CHROME_PATH,AGENT_HEADER
from utils import (
    WebControlMixin
)

class NovelPost(WebControlMixin):
    def login_required(f):
        def _wrapper(self, *args, **keywords):
            if self.is_login:
                return f(self,*args,**keywords)
            else:
                raise Exception("not login")
        return _wrapper
    def access(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        service = Service(executable_path=CHROME_PATH)
        self.driver=webdriver.Chrome(service=service,options=options)
        self.access_page(self.top_url)
        #print(self.driver.page_source)
    
    def login(self, user, password):
        self.access()
        self.login_browser(user,password)
        self.login_session(user,password)
        
        self.is_login=True
        #id=userid
        
    def login_browser(self,user,password):
        self.click_with_update(self.login_btn_xpath)
        self.send_data(user,self.username_name,3)
        self.send_data(password,self.password_name,3)
        self.click_with_update(self.submit_xpath,is_page_update=True)
        
        
    
    def login_session(self,user,password, **kwargs):
        payload={
            self.user_element:user,
            self.password_element:password,"location":"/"
        }
        if self.button_element:
            payload[self.button_element] = self.login_value
        if "session" in kwargs:
            session = kwargs.get("session")
        else:
            session = requests.session()
        
        headers = AGENT_HEADER
        if "headers" in kwargs:
            headers.update(kwargs.get("headers"))
        r=session.post(self.login_url,data=payload,headers=headers)
        if r.status_code!=200:
            pass
        
        self.session=session
        return session
    
    @login_required
    def user_top(self):
        self.access_page(self.user_top_url)
    
