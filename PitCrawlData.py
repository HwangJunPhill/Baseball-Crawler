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
            if str(rows[x][1]) == profile['이름']:
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

    def crawl_season(self):
        for x in range(1, 17):
            titles = self.html.xpath('//*[@id="mArticle"]/div/div[3]/div/table/thead/tr/th[{}]'.format(x))
            values = self.html.xpath('//*[@id="mArticle"]/div/div[3]/div/table/tbody/tr/td[{}]'.format(x))

            if titles == []:
                return
            else:
                season_data[titles[0].text] = values[0].text.strip()


    def db_season(self):
        sql = 'select * from `sports`.`pitseason_record`'
        curs.execute(sql)
        rows = curs.fetchall()

        if len(rows) == 0:
            sql = """
            INSERT INTO `sports`.`pitseason_record` (`G`, `W`, `L`, `S`, `HLD`, `IP`, `NP`, `H`, `HR`, `K`, `BB`, `R`, `ER`, `ERA`, `WHIP`, `QS` ) VALUES (%(경기)s, %(승)s, %(패)s, %(세)s, %(홀)s, %(이닝)s, %(투구수)s, %(피안타)s, %(피홈런)s, %(탈삼진)s, %(사사구)s, %(실점)s, %(자책)s, %(평균자책)s, %(WHIP)s, %(QS)s)
            """

            curs.execute(query=sql,
                         args={'경기': season_data['경기'], '승': season_data['승'], '패': season_data['패'],
                               '세': season_data['세이브'], '홀': season_data['홀드'], '이닝': season_data['이닝'],
                               '투구수': season_data['투구수'], '피안타': season_data['피안타'], '피홈런': season_data['피홈런'],
                               '탈삼진': season_data['탈삼진'], '사사구': season_data['사사구'], '실점': season_data['실점'],
                               '자책': season_data['자책'], '평균자책': season_data['평균자책'], 'WHIP': season_data['WHIP'],
                               'QS': season_data['QS']})

            tmp.commit()

            return

        else:
            for x in range(len(rows)):
                if key['key'] == rows[x][0]:
                    sql = """
                        UPDATE `sports`.`pitseason_record` SET `G` = %(경기)s, `W` = %(승)s, `L` = %(패)s, `S` = %(세)s,
                        `HLD` = %(홀)s, `IP` = %(이닝)s, `NP` = %(투구수)s, `H` = %(피안타)s, `HR` = %(피홈런)s, `K` = %(탈삼진)s,
                        `BB` = %(사사구)s, `R` = %(실점)s, `ER` = %(자책)s, `ERA` = %(평균자책)s, `WHIP` = %(WHIP)s,
                        `QS` = %(QS)s WHERE `No` =%(No)s
                    """

                    curs.execute(query=sql,
                                 args={'경기': season_data['경기'], '승': season_data['승'], '패': season_data['패'],
                                       '세': season_data['세이브'], '홀': season_data['홀드'], '이닝': season_data['이닝'],
                                       '투구수': season_data['투구수'], '피안타': season_data['피안타'], '피홈런': season_data['피홈런'],
                                       '탈삼진': season_data['탈삼진'], '사사구': season_data['사사구'], '실점': season_data['실점'],
                                       '자책': season_data['자책'], '평균자책': season_data['평균자책'],
                                       'WHIP': season_data['WHIP'],
                                       'QS': season_data['QS'], 'No': key['key']})

                    tmp.commit()
                    return

        sql = """
            INSERT INTO `sports`.`pitseason_record` (`G`, `W`, `L`, `S`, `HLD`, `IP`, `NP`, `H`, `HR`, `K`, `BB`, `R`, `ER`,
            `ERA`, `WHIP`, `QS` ) VALUES (%(경기)s, %(승)s, %(패)s, %(세)s, %(홀)s, %(이닝)s, %(투구수)s, %(피안타)s, %(피홈런)s,
            %(탈삼진)s, %(사사구)s, %(실점)s, %(자책)s, %(평균자책)s, %(WHIP)s, %(QS)s)
        """

        curs.execute(query=sql,
                     args={'경기': season_data['경기'], '승': season_data['승'], '패': season_data['패'],
                           '세': season_data['세이브'], '홀': season_data['홀드'], '이닝': season_data['이닝'],
                           '투구수': season_data['투구수'], '피안타': season_data['피안타'], '피홈런': season_data['피홈런'],
                           '탈삼진': season_data['탈삼진'], '사사구': season_data['사사구'], '실점': season_data['실점'],
                           '자책': season_data['자책'], '평균자책': season_data['평균자책'], 'WHIP': season_data['WHIP'],
                           'QS': season_data['QS']})

        tmp.commit()

    def crawl_daily(self):
        for x in range(1,20):
            titles = self.html.xpath('//*[@id="mArticle"]/div/div[3]/div/div[1]/table/thead/tr/th[{}]'.format(x))
            values = self.html.xpath('//*[@id="mArticle"]/div/div[3]/div/div[1]/table/tbody/tr[1]/td[{}]'.format(x))

            if titles == []:
                return
            else:
                daily_data[titles[0].text] = values[0].text.strip()

    def db_daily(self):
            if daily_data == {}:
                return
            sql = 'select * from `sports`.`pitdaily_record`'
            curs.execute(sql)
            rows = curs.fetchall()

            if len(rows) == 0:
                    sql = """
                    INSERT INTO `sports`.`pitdaily_record` (`Date`,`Opponent`, `W`, `L`, `S`, `HLD`, `IP`, `NP`, `H`, `HR`, `K`, `BB`, `R`, `ER`,`WHIP` ) VALUES (%(날짜)s, %(상대)s, %(승)s, %(패)s, %(세)s, %(홀)s, %(이닝)s, %(투구수)s, %(피안타)s, %(피홈런)s, %(탈삼진)s, %(사사구)s, %(실점)s, %(자책)s, %(WHIP)s)
                    """

                    curs.execute(query=sql,
                                 args={'날짜': daily_data['날짜'], '상대': daily_data['상대'], '승': daily_data['승'], '패': daily_data['패'],
                                       '세': daily_data['세이브'], '홀': daily_data['홀드'], '이닝': daily_data['이닝'],
                                       '투구수': daily_data['투구수'], '피안타': daily_data['피안타'], '피홈런': daily_data['피홈런'],
                                       '탈삼진': daily_data['탈삼진'], '사사구': daily_data['사사구'], '실점': daily_data['실점'],
                                       '자책': daily_data['자책'],
                                       'WHIP': daily_data['WHIP']})

                    tmp.commit()

                    return

            else:
                for x in range(len(rows)):
                    if key['key'] == rows[x][0]:
                        sql = """
                            UPDATE `sports`.`pitdaily_record` SET `Date` = %(날짜)s,`Opponent` = %(상대)s, `W` = %(승)s, `L` = %(패)s, `S` = %(세)s,
                            `HLD` = %(홀)s, `IP` = %(이닝)s, `NP` = %(투구수)s, `H` = %(피안타)s, `HR` = %(피홈런)s, `K` = %(탈삼진)s,
                            `BB` = %(사사구)s, `R` = %(실점)s, `ER` = %(자책)s, `WHIP` = %(WHIP)s WHERE `No` =%(No)s
                        """
                        curs.execute(query=sql,
                                     args={'날짜': daily_data['날짜'], '상대': daily_data['상대'], '승': daily_data['승'],
                                           '패': daily_data['패'],
                                           '세': daily_data['세이브'], '홀': daily_data['홀드'], '이닝': daily_data['이닝'],
                                           '투구수': daily_data['투구수'], '피안타': daily_data['피안타'], '피홈런': daily_data['피홈런'],
                                           '탈삼진': daily_data['탈삼진'], '사사구': daily_data['사사구'], '실점': daily_data['실점'],
                                           '자책': daily_data['자책'],
                                           'WHIP': daily_data['WHIP'], 'No': key['key']})

                        tmp.commit()
                        return

                sql = """
                INSERT INTO `sports`.`pitdaily_record` (`Date`,`Opponent`, `W`, `L`, `S`, `HLD`, `IP`, `NP`, `H`, `HR`, `K`, `BB`, `R`, `ER`,`WHIP` ) VALUES (%(날짜)s, %(상대)s, %(승)s, %(패)s, %(세)s, %(홀)s, %(이닝)s, %(투구수)s, %(피안타)s, %(피홈런)s, %(탈삼진)s, %(사사구)s, %(실점)s, %(자책)s, %(WHIP)s)
                """

                curs.execute(query=sql,
                             args={'날짜': daily_data['날짜'], '상대': daily_data['상대'], '승': daily_data['승'],
                                   '패': daily_data['패'],
                                   '세': daily_data['세이브'], '홀': daily_data['홀드'], '이닝': daily_data['이닝'],
                                   '투구수': daily_data['투구수'], '피안타': daily_data['피안타'], '피홈런': daily_data['피홈런'],
                                   '탈삼진': daily_data['탈삼진'], '사사구': daily_data['사사구'], '실점': daily_data['실점'],
                                   '자책': daily_data['자책'],
                                   'WHIP': daily_data['WHIP']})
                tmp.commit()

    def crawl_total(self):
        for x in range(3, 19):
            title = self.html2.xpath('//*[@id="mArticle"]/div/div[3]/div/table/thead/tr/th[{}]'.format(x))
            value = self.html2.xpath('//*[@id="mArticle"]/div/div[3]/div/table/tfoot/tr/td[{}]'.format(x))

            total_data[title[0].text] = value[0].text.strip()

    def db_total(self):

        sql = 'select * from `sports`.`pittotal_record`'
        curs.execute(sql)
        rows = curs.fetchall()

        if len(rows) == 0:
            sql = """
            INSERT INTO `sports`.`pittotal_record` (`G`, `W`, `L`, `S`, `HLD`, `IP`, `NP`, `H`, `HR`, `K`, `BB`, `R`, `ER`, `ERA`, `WHIP`, `QS` ) VALUES (%(경기)s, %(승)s, %(패)s, %(세)s, %(홀)s, %(이닝)s, %(투구수)s, %(피안타)s, %(피홈런)s, %(탈삼진)s, %(사사구)s, %(실점)s, %(자책)s, %(평균자책)s, %(WHIP)s, %(QS)s)
            """

            curs.execute(query=sql,
                         args={'경기': total_data['경기'], '승': total_data['승'], '패': total_data['패'],
                               '세': total_data['세이브'], '홀': total_data['홀드'], '이닝': total_data['이닝'],
                               '투구수': total_data['투구수'], '피안타': total_data['피안타'], '피홈런': total_data['피홈런'],
                               '탈삼진': total_data['탈삼진'], '사사구': total_data['사사구'], '실점': total_data['실점'],
                               '자책': total_data['자책'], '평균자책': total_data['평균자책'], 'WHIP': total_data['WHIP'],
                               'QS': total_data['QS']})

            tmp.commit()

            return

        else:
            for x in range(len(rows)):
                if key['key'] == rows[x][0]:
                    sql = """
                        UPDATE `sports`.`pittotal_record` SET `G` = %(경기)s, `W` = %(승)s, `L` = %(패)s, `S` = %(세)s,
                        `HLD` = %(홀)s, `IP` = %(이닝)s, `NP` = %(투구수)s, `H` = %(피안타)s, `HR` = %(피홈런)s, `K` = %(탈삼진)s,
                        `BB` = %(사사구)s, `R` = %(실점)s, `ER` = %(자책)s, `ERA` = %(평균자책)s, `WHIP` = %(WHIP)s,
                        `QS` = %(QS)s WHERE `No` =%(No)s
                    """

                    curs.execute(query=sql,
                                 args={'경기': total_data['경기'], '승': total_data['승'], '패': total_data['패'],
                                       '세': total_data['세이브'], '홀': total_data['홀드'], '이닝': total_data['이닝'],
                                       '투구수': total_data['투구수'], '피안타': total_data['피안타'], '피홈런': total_data['피홈런'],
                                       '탈삼진': total_data['탈삼진'], '사사구': total_data['사사구'], '실점': total_data['실점'],
                                       '자책': total_data['자책'], '평균자책': total_data['평균자책'],
                                       'WHIP': total_data['WHIP'],
                                       'QS': total_data['QS'], 'No': key['key']})

                    tmp.commit()
                    return

        sql = """
            INSERT INTO `sports`.`pittotal_record` (`G`, `W`, `L`, `S`, `HLD`, `IP`, `NP`, `H`, `HR`, `K`, `BB`, `R`, `ER`,
            `ERA`, `WHIP`, `QS` ) VALUES (%(경기)s, %(승)s, %(패)s, %(세)s, %(홀)s, %(이닝)s, %(투구수)s, %(피안타)s, %(피홈런)s,
            %(탈삼진)s, %(사사구)s, %(실점)s, %(자책)s, %(평균자책)s, %(WHIP)s, %(QS)s)
        """

        curs.execute(query=sql,
                     args={'경기': total_data['경기'], '승': total_data['승'], '패': total_data['패'],
                           '세': total_data['세이브'], '홀': total_data['홀드'], '이닝': total_data['이닝'],
                           '투구수': total_data['투구수'], '피안타': total_data['피안타'], '피홈런': total_data['피홈런'],
                           '탈삼진': total_data['탈삼진'], '사사구': total_data['사사구'], '실점': total_data['실점'],
                           '자책': total_data['자책'], '평균자책': total_data['평균자책'], 'WHIP': total_data['WHIP'],
                           'QS': total_data['QS']})

        tmp.commit()

    def cal_stat(self):

        sql = 'select * from `sports`.`pittotal_record` where No = %(번호)s'
        curs.execute(query=sql, args={'번호': key['key']})
        rows = curs.fetchall()

        sql = 'select * from `sports`.`pitseason_record` where No = %(번호)s'
        curs.execute(query=sql, args={'번호': key['key']})
        season_rows = curs.fetchall()

        ip = rows[0][6]
        if '/' in ip:
            i = int(ip[:len(ip)-3])
            j = int(ip[-3])
            ip=(i + j / 3)

        else:
            ip = int(ip)

        stat['control'] = round(40 / (rows[0][11] / ip))
        stat['power'] = round((rows[0][10]/ip)* 10000/85)
        stat['def'] = round(rows[0][13]/rows[0][12] * 100)
        stat['physical'] = round(season_rows[0][7]/season_rows[0][1])

    def db_stat(self):
        sql = 'select * from `sports`.`pitstat` where No = %(번호)s'
        curs.execute(query=sql, args={'번호':key['key']})
        rows = curs.fetchall()

        if len(rows) == 0:
            print('add')
            sql = """
                insert into `sports`.`pitstat` (`Control`, `Power`, `Physical`, `Def`)
                values (%(제구)s, %(구위)s, %(체력)s, %(수비)s)
                """
            curs.execute(query=sql,
                         args={'제구': stat['control'], '구위': stat['power'], '체력': stat['physical'], '수비': stat['def']})

        else:
            sql = """
                update `sports`.`pitstat` set `Control` = %(제구)s, `Power` = %(구위)s, `Physical` = %(체력)s, `Def` = %(수비)s
                where No = %(번호)s
                """
            curs.execute(query=sql, args={'제구': stat['control'], '구위': stat['power'], '체력': stat['physical'], '수비': stat['def'], '번호':key['key']})

        tmp.commit()


if __name__ == '__main__':
    cmsim = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=10316',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=10316']

    wccha = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=10162',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=10162']

    jhwon = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=10124',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=10124']

    wrjeong = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=10059',
               'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=10059']

    hkwon = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=9934',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=9934']

    hhhan = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=433939',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=433939']

    swpark = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=973425',
              'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=973425']

    hjyang = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=10268',
              'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=10268']

    jkryu = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=799413',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=799413']

    ypko = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=973495',
            'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=973495']

    shyoon = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=10032',
              'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=10032']

    ysbae = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=9858',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=9858']

    wjjang = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=10034',
              'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=10034']

    cylim = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=5601',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=5601']

    shkim = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=10148',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=10148']

    hslee = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=10145',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=10145']

    shjang = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=10234',
              'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=10234']

    pjjang = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_main.daum?person_id=1098477',
              'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_pit_rechist.daum?person_id=1098477']



    player = [cmsim, wccha, jhwon, wrjeong, hkwon, hhhan, swpark, hjyang, jkryu, ypko, shyoon, ysbae, wjjang, cylim,
              shkim, hslee, shjang, pjjang]

    test = [wccha]
    for x in player:
        a = basic(x)

        a.crawl_profile()
        a.crawl_daily()
        a.crawl_season()
        a.crawl_total()


        a.db_profile()
        a.db_daily()
        a.db_season()
        a.db_total()

        a.cal_stat()
        a.db_stat()