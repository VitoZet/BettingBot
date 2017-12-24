import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen


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
        html_tree = urlopen(html).read()
        bsObj = BeautifulSoup(html_tree, 'lxml')
        event_title = bsObj.title.text[8:-56]  # print Арамбагх КС - Абахани Лимитед
        # event_country = bsObj.h1.text[:-6] #Чемпионат Марокко : Кавкаб - Магреб Атлетик
        event_country = bsObj.h1.text[:19]  # Чемпионат Марокко
        event_timer_split = bsObj.findAll('div', {'class': 'game_count_wrap'})[0].text.split()  # ['0', ':', '0', 'идёт', '2-й', 'Тайм.', 'прошло:', '78', 'мин']
        event_timer_str = ' '.join(event_timer_split)  # 0 : 0 идёт 2-й Тайм. прошло: 58 мин
        # total = bsObj.findAll('div', {'data-gameid': '4'})
        total = bsObj.findAll('div', {'id': 'allBetsTable'})
        # total = bsObj.findAll('div', {'class': 'bet-title'})

        print(total)
        print(event_country)
        print(event_title)
        print(event_timer_str)


if __name__ == '__main__':
    # parser = BettingParser('https://1xstavka.ru/live/Football/')
    parser = BettingParser(
        'https://1xstavka.ru/live/Football/31429-Morocco-Botola/148738818-KAC-Marrakech-Moghreb-Tetouan/')
    # parser = BettingParser('https://1xstavka.ru/live/Football/31429-Morocco-Botola/148738818-KAC-Marrakech-Moghreb-Tetouan/')
    page = parser.get_page()
    # parser.parse_all_events('https://1xstavka.ru/live/Football/')
    parser.parse_event(
        'https://1xstavka.ru/live/Football/31429-Morocco-Botola/148738818-KAC-Marrakech-Moghreb-Tetouan/')
