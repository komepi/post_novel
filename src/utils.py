from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from calendar import Calendar
from datetime import datetime

from config import MSG_NOT_FOUD_ELEMENT

XPATH = 0
ID = 1
CLASS = 2
NAME = 3
METHOD_LIST = [XPATH, ID, CLASS, NAME]
INDEX = 0
VALUE = 1
TEXT = 2
SELECT_LIST = [INDEX, VALUE, TEXT]


class WebControlMixin:
    def click_with_update(self, path, method=XPATH,is_page_update=False,span_time=1.0):
        self.find_element(method, path).click()
        if is_page_update:
            WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located)

    def access_page(self, url,is_page_update=True):
        self.driver.get(url)
        if is_page_update:
            WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located)

    def find_element(self, method, path):
        m=self._select_method(method)
        return self.driver.find_element(m,path)

    def send_data(self,  data, path, method=XPATH):
        m=self._select_method(method)
        try:
            element=self.driver.find_element(m, path)
        except:
            print(MSG_NOT_FOUD_ELEMENT % path)
            return
        element.send_keys(data)

    def _select_method(self,method):
        """検索手法を探す

        Args:
            method (int): 検索手法の番号

        Raises:
            KeyError: 定められた検索手法番号以外の番号

        Returns:
            by: 検索手法
        """
        #print("method:{}".format(type(method)))
        if method not in METHOD_LIST:
            raise KeyError
        if method == XPATH:
            m = By.XPATH
        elif method == ID:
            m = By.ID
        elif method == CLASS:
            m = By.CLASS_NAME
        elif method == NAME:
            m = By.NAME

        return m

    def select_calender(self,  dates):
        """datepickerを用いて日付を選択する

        Args:
            dates (list[tk.Entry])): 日付のリスト
        """
        if dates:
            year=dates[0].get()
            month = dates[1].get()
            day = dates[2].get()
            self.click_with_update( "reserve_date",method=NAME,is_check=True) # datepickerを開く
            self.select_drop( str(year),"//*[@id=\"ui-datepicker-div\"]/div[1]/div/select[1]",
                    method=XPATH,select_by=VALUE)# 年の選択
            self.select_drop( str(int(month)-1).zfill(2),"//*[@id=\"ui-datepicker-div\"]/div[1]/div/select[2]",
                    method=XPATH,select_by=VALUE) # 月の選択

            ans = 0
            day_of_week = 0
            date = datetime(int(year),int(month),int(day))
            cl = Calendar(firstweekday=6)
            month_cl = cl.monthdays2calendar(date.year,date.month)
            week_num = 1

            for week in month_cl:
                for day in week:
                    if day[0] == date.day:
                        ans = week_num
                        day_of_week = day[1]
                week_num+=1

            day_of_week = (day_of_week + 2) % 7
            if day_of_week == 0:
                day_of_week = 7
            xpath = "//*[@id=\"ui-datepicker-div\"]/table/tbody/tr[" + str(ans) + "]/td[" + str(day_of_week) + "]/a"
            self.click_with_update( xpath,method =XPATH,is_check=True) # 日付の選択

    def select_drop(self,  data,path,method=0,select_by=0,memo=None):
        """ドロップダウンから選択する
        method -> 0:xpath, 1:id, 2:class, 3:name
        select_by -> 0:index, 1:value, 2:text
        Args:
            data (obj): 選択に用いるデータ
            path (str): 要素を検索するデータ
            method (int, optional): 検索手法. Defaults to 0.
            select_by (int, optional): 選択手法. Defaults to 0.
            memo (str, optional): 何を選択したかメモ用. Defaults to None.
        """
        try:
            m = self._select_method(method)
        except KeyError:
            print("testerror")

        select_obj = self.driver.find_element(m,path)

        select = Select(select_obj)
        self._select_by(select,select_by,data)

    def _select_by(self, select,method,value):
        """選択する

        Args:
            select (select): selectオブジェクト
            method (int): 選択手法
            value (obj): 選択に用いるデータ

        Raises:
            KeyError: 定められた選択手法以外の番号

        """
        if method not in SELECT_LIST:
            raise KeyError
        if method == INDEX:
            return select.select_by_index(value)
        elif method == VALUE:
            print("select by value to " + value)
            select.select_by_value(value)
        elif method == TEXT:
            select.select_by_visible_text(value)

    def select_drop(self, d, data,path,method=0,select_by=0,memo=None):
        """ドロップダウンから選択する
        method -> 0:xpath, 1:id, 2:class, 3:name
        select_by -> 0:index, 1:value, 2:text
        Args:
            data (obj): 選択に用いるデータ
            path (str): 要素を検索するデータ
            method (int, optional): 検索手法. Defaults to 0.
            select_by (int, optional): 選択手法. Defaults to 0.
            memo (str, optional): 何を選択したかメモ用. Defaults to None.
        """
        try:
            m = self._select_method(method)
        except KeyError:
            print("testerror1")

        select_obj = d.find_element(m,path)

        select = Select(select_obj)
        self._select_by(select,select_by,data)