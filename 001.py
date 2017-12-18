import requests
import lxml.html


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
        html_tree = lxml.html.fromstring(html)
        parse_events_url = html_tree.xpath(".//a[@class='c-events__name']")
        for u in parse_events_url:
            list_url_events.append('https://1xstavka.ru/' + u.get('href'))
        return list_url_events


if __name__ == '__main__':
    parser = BettingParser('https://1xstavka.ru/live/Football/')
    page = parser.get_page()
    parser.parse_all_events(page)
