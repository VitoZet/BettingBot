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
        parse_events_url = html_tree.xpath(".//div[@class='c-events__item']")
        # parse_events_url = html_tree.xpath(".//a[@class='c-events__name']")
        # score = html_tree.xpath(".//div[@class='c-events__score']").text_content()
        for u in parse_events_url:
            # print(u.xpath(".//span[@class='c-events__fullScore']")[0].text_content())
            # print(u.xpath("//*[@id='games_content']/div/div/div[2]/div[2]/div/div[4]/div[1]/span[2]"))
            list_url_events.append('https://1xstavka.ru/' + u.xpath(".//a[@class='c-events__name']")[0].get('href'))
        # print(score)
        print(list_url_events)
        return list_url_events

    def parse_event(self, html):
        html_tree = lxml.html.fromstring(html)
        event_title = html_tree.xpath('/html/head/title/text()')[0][8:-56] # print Арамбагх КС - Абахани Лимитед
        event_country = html_tree.xpath('//h1[@id="page_title"]')[0].text_content().strip().split(':')[0][:-1] #Чемпионат Египта. Премьер-лига
        event_timer_split = html_tree.xpath('//div[@class="game_count_wrap"]')[0].text_content().split() # ['0', ':', '0', 'идёт', '1-й', 'Тайм.', 'прошло:', '25', 'мин']
        event_timer_str = ' '.join(event_timer_split) #0 : 0 идёт 2-й Тайм. прошло: 58 мин
        # coef_bet = html_tree.xpath('//div[@data-gameid="148424184"]') #//div[@class="c-events main_game"]')
        # coef_bet = html_tree.xpath('//*[@id="games_content"]/div/div')    #[1].text_content().split()
        # coef_bet = html_tree.xpath('//div[@id="maincontent"]//div[@id="sports_page"]//div[@id="hottest_games"]//div[@class="game_content_line on_main "]')    #[1].text_content().split()
        coef_bet = html_tree.xpath('//div[@id="allBetsTable"]')    #[1].text_content().split()
        # coef_bet2 = coef_bet.xpath('//')

        #.//div[@data-gameid="4"]
        print(event_country)
        print(event_title)
        print(event_timer_str)
        print(coef_bet)


if __name__ == '__main__':
    # parser = BettingParser('https://1xstavka.ru/live/Football/')
    # parser = BettingParser('https://1xstavka.ru/live/Football/120705-Hazfi-Cup/148410103-Esteghlal-Khuzestan-Tractor-Sazi/')
    parser = BettingParser('https://1xstavka.ru/live/Football/119235-Germany-DFB-Pokal/148431915-1-FSV-Mainz-05-VfB-Stuttgart/')
    page = parser.get_page()
    # parser.parse_all_events(page)
    parser.parse_event(page)
