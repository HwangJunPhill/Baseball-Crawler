import requests
from lxml import etree
import pymysql
from bs4 import BeautifulSoup
import urllib.request

tmp = pymysql.connect(host='localhost', user='root', password='', db='sports', charset='utf8')
curs = tmp.cursor()

key = {}

season_data = {}
total_data = {}
daily_data = {}
profile = {}
stat = {}


class basic():
    def __init__(self, link):
        self.url = link[0]
        self.respose = requests.get(self.url)
        self.html = etree.HTML(self.respose.text)

        self.url2 = link[1]
        self.respose = requests.get(self.url2)
        self.html2 = etree.HTML(self.respose.text)

    def crawl_profile(self):
        #이름, 배번, 팀
        profile['이름'] = self.html.xpath('//*[@id="mArticle"]/div/div[2]/div[2]/strong')[0].text
        profile['배번'] = self.html.xpath('//*[@id="mArticle"]/div/div[2]/div[2]/strong/span[1]')[0].text
        profile['팀'] = self.html.xpath('//*[@id="mArticle"]/div/div[2]/div[2]/strong/span[3]')[0].text

        #사진 구하기
        URL = urllib.request.Request(self.url)
        data = urllib.request.urlopen(URL).read()
        soup = BeautifulSoup(data, 'html.parser')
        th = soup.findAll('img')

        for x in th:
            string = x.get('class')
            if string == None:
                pass
            elif len(string) == 2 and string[1] == 'img-player-pic':
                string = x.get('src')
                profile['img'] = string

        #나머지 정보들
        for x in range(5):
            profile_label = self.html.xpath('//*[@id="mArticle"]/div/div[2]/div[3]/dl[{}]/dt'.format(x))
            profile_value = self.html.xpath('//*[@id="mArticle"]/div/div[2]/div[3]/dl[{}]/dd'.format(x))

            if profile_label:
                profile[profile_label[0].text.strip(" :")] = profile_value[0].text.strip()

        print(profile)

    # 프로필 DB 삽입
    def db_profile(self):
        sql = 'select * from `sports`.`pitprofile`'
        curs.execute(sql)
        rows = curs.fetchall()

        if len(rows) == 0:
            key['key'] = 1
            sql = """
                    INSERT INTO `sports`.`pitprofile` (`Name`, `Number`, `Team`, `Debut`, `Born`, `Position`, `Body`, `Photo`)
                     VALUES (%(이름)s, %(배번)s, %(팀)s, %(데뷔)s, %(출생)s, %(포지션)s, %(신체)s, %(사진)s)
                    """

            curs.execute(query=sql,
                         args={'이름': profile['이름'], '배번': profile['배번'], '팀': profile['팀'], '데뷔': profile['데뷔'], '출생': profile['출생'], '포지션': profile['포지션'],
                               '신체': profile['신체'], '사진':profile['img']})
            tmp.commit()

            return

        for x in range (len(rows)):
            if str(rows[x][1]) == profile['name']:
                key['key'] = rows[x][0]
                return

        key['key'] += 1

        sql = """
        INSERT INTO `sports`.`pitprofile` (`Name`, `Number`, `Team`, `Debut`, `Born`, `Position`, `Body`, `Photo`)
        VALUES (%(이름)s, %(배번)s, %(팀)s, %(데뷔)s, %(출생)s, %(포지션)s, %(신체)s, %(사진)s)
        """

        curs.execute(query=sql,
                     args={'이름': profile['이름'], '배번': profile['배번'], '팀':profile['팀'], '데뷔': profile['데뷔'], '출생': profile['출생'], '포지션': profile['포지션'],
                           '신체': profile['신체'], '사진':profile['img']})
        tmp.commit()

    def crawl_daily(self):
        pass

    def db_daily(self):
        pass

    def crawl_season(self):
        pass

    def db_season(self):
        pass

    def crawl_total(self):
        pass

    def db_total(self):
        pass


if __name__ == '__main__':
    cmsim = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=10316',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=10316']

    a = basic(cmsim)
    a.crawl_profile()
    a.db_profile()