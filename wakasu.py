import requests
from bs4 import BeautifulSoup
import re
from dateutil import parser
from datetime import date
from typing import Type
from camp_site import CampSite

class Wakasu():
    camp_site: Type[CampSite] = None

    def __init__(self, campSite: CampSite) -> None:
        self.camp_site = campSite

    def check_availability(self, check_date: date) -> bool:
        available_dates_list = self.__get_available_dates_list()

        return check_date in available_dates_list
    
    def __get_available_dates_list(self) -> list[date]:
        ua = 'Mozilla/5.0'
        load_url = self.camp_site.url
        html = requests.get(load_url, headers={'User-Agent': ua})
        soup = BeautifulSoup(html.content, "html.parser")

        months = soup.find_all(class_="month")
        calendar = soup.find_all(class_="calendar")

        available_dates = []

        for i, element in enumerate(calendar):
            icons = element.find_all(class_="icon")
            year_month = months[i].getText()

            # 休場日はiconsに入っていないのでそのまま無視する
            for icon in icons:
                if(icon.find("img")):
                    year_pattern = re.compile(r'\d{4}')
                    year = re.search(year_pattern, year_month).group()
                    month = year_month.split('年')[1].replace('月', '')

                    day = icon.find_previous_sibling("label").getText().rstrip('日')
                    dt = parser.parse('{}-{}-{}'.format(year, month, day)).date()
                    isAvailable = icon.find("img").get("alt")
                    # ⚪︎と△の場合あり
                    if (isAvailable != "空きなし"):
                        available_dates.append(dt)
        return available_dates
