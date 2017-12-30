import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver


class BettingParser:
    def __init__(self, base_url):
        self.base_url = base_url
        self.last_time = ''

    def get_page(self):

        try:
            res = requests.get(self.base_url)
        except requests.ConnectionError:
            print('no')
            return

        if res.status_code < 400:
            return res.content

    def parse_all_events(self, html):  # возвращает список ссылок live событий
        list_url_events = []
        html_tree = urlopen(html).read()
        bsObj = BeautifulSoup(html_tree, 'lxml')
        soup_url_events = bsObj.findAll("a", {"class": "c-events__name"})
        for u in soup_url_events:
            list_url_events.append(u.get('href'))
        return list_url_events

    def parse_event(self, html):
        driver = webdriver.Chrome('C:/ChromeDriver/chromedriver.exe')
        driver.get(html)
        event_country = driver.find_element_by_xpath('//*[@id="line_breadcrumbs"]').text[23:]
        event_time = driver.find_element_by_xpath('//*[@class="db-sport__top"]').text
        print(event_country)
        print(event_time)
        if driver.find_element_by_xpath('//*[@id="allBetsTable"]/div[1]/div[3]/div/div[2]/div[1]/span[1]').text == '1.5 Б':
            print('кэф ТБ 0,5 = ' + driver.find_element_by_xpath('//*[@id="allBetsTable"]/div[1]/div[3]/div/div[2]/div[1]/span[2]/i').text)


if __name__ == '__main__':

    html_event = 'https://1xstavka.ru/live/Football/926931-Antigua-and-Barbuda-Premier-Division/149029224-SAP-Tryum/'
    parser = BettingParser(html_event)
    page = parser.get_page()
    # parser.parse_all_events('https://1xstavka.ru/live/Football/')
    parser.parse_event(html_event)
