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
rank = {}
stat = {}


class basic():
    def __init__(self, link):
        self.url = link[0]
        self.respose = requests.get(self.url)
        self.html = etree.HTML(self.respose.text)

        self.url2 = link[1]
        self.respose = requests.get(self.url2)
        self.html2 = etree.HTML(self.respose.text)

        self.name = self.html.xpath('//*[@id="mArticle"]/div/div[2]/div[2]/strong')[0].text



    # 프로필
    def crawl_profile(self):
        profile['이름'] = self.name
        profile['배번'] = self.html.xpath('//*[@id="mArticle"]/div/div[2]/div[2]/strong/span[1]')[0].text
        profile['팀'] = self.html.xpath('//*[@id="mArticle"]/div/div[2]/div[2]/strong/span[3]')[0].text

        for x in range(5):
            profile_label = self.html.xpath('//*[@id="mArticle"]/div/div[2]/div[3]/dl[{}]/dt'.format(x))
            profile_value = self.html.xpath('//*[@id="mArticle"]/div/div[2]/div[3]/dl[{}]/dd'.format(x))

            if profile_label:
                profile[profile_label[0].text.strip(" :")] = profile_value[0].text.strip()

    # 프로필 DB 삽입
    def db_profile(self):
        sql = 'select * from `sports`.`profile`'
        curs.execute(sql)
        rows = curs.fetchall()

        if len(rows) == 0:
            key['key'] = 1
            sql = """
                    INSERT INTO `sports`.`profile` (`Name`, `Number`, `Team`, `Debut`, `Born`, `Position`, `Body`, `Photo`)
                     VALUES (%(이름)s, %(배번)s, %(팀)s, %(데뷔)s, %(출생)s, %(포지션)s, %(신체)s, %(사진)s)
                    """

            curs.execute(query=sql,
                         args={'이름': profile['이름'], '배번': profile['배번'], '팀': profile['팀'], '데뷔': profile['데뷔'], '출생': profile['출생'], '포지션': profile['포지션'],
                               '신체': profile['신체'], '사진':profile['img']})
            tmp.commit()

            return

        for x in range (len(rows)):
            if str(rows[x][1]) == self.name:
                key['key'] = rows[x][0]
                return

        key['key'] += 1

        sql = """
        INSERT INTO `sports`.`profile` (`Name`, `Number`, `Team`, `Debut`, `Born`, `Position`, `Body`, `Photo`)
        VALUES (%(이름)s, %(배번)s, %(팀)s, %(데뷔)s, %(출생)s, %(포지션)s, %(신체)s, %(사진)s)
        """

        curs.execute(query=sql,
                     args={'이름': profile['이름'], '배번': profile['배번'], '팀':profile['팀'], '데뷔': profile['데뷔'], '출생': profile['출생'], '포지션': profile['포지션'],
                           '신체': profile['신체'], '사진':profile['img']})
        tmp.commit()

    # 시즌 기록
    def crawl_season(self):

        for x in range(1, 17):
            titles = self.html.xpath('//*[@id="mArticle"]/div/div[3]/div/table/thead/tr/th[{}]'.format(x))
            values = self.html.xpath('//*[@id="mArticle"]/div/div[3]/div/table/tbody/tr/td[{}]'.format(x))

            if titles == []:
                return
            else:
                season_data[titles[0].text] = values[0].text.strip()

    # 시즌 기록 DB 삽입
    def db_season(self):
        if season_data == {}:
            return

        sql = 'select * from `sports`.`season_record`'
        curs.execute(sql)
        rows = curs.fetchall()

        if len(rows) == 0:
            sql = """
            INSERT INTO `sports`.`season_record` (`G`, `PA`, `AB`, `H`, `2B`, `3B`, `HR`, `RBI`, `R`, `SB`, `BB`, `SO`, `AVG`, `OBA`, `SA`, `OPS` ) VALUES (%(경기)s, %(타석)s, %(타수)s, %(안타)s, %(2루타)s, %(3루타)s, %(홈런)s, %(타점)s, %(득점)s, %(도루)s, %(사사구)s, %(삼진)s, %(타율)s, %(출루율)s, %(장타율)s, %(OPS)s)
            """

            curs.execute(query=sql,
                         args={'경기': season_data['경기'], '타석': season_data['타석'], '타수': season_data['타수'], '안타': season_data['안타'], '2루타': season_data['2타'], '3루타': season_data['3타'], '홈런': season_data['홈런'], '타점': season_data['타점'], '득점': season_data['득점'], '도루': season_data['도루'], '사사구': season_data['사사구'], '삼진': season_data['삼진'], '타율': season_data['타율'], '출루율': season_data['출루율'], '장타율': season_data['장타율'], 'OPS': season_data['OPS']})

            tmp.commit()

            return

        else:
            for x in range(len(rows)):
                if key['key'] == rows[x][0]:
                    sql = """
                    UPDATE `sports`.`season_record` SET `G` = %(경기)s, `PA` = %(타석)s, `AB` = %(타수)s, `H` = %(안타)s, `2B` = %(2루타)s, `3B` = %(3루타)s, `HR` = %(홈런)s, `RBI` = %(타점)s, `R` = %(득점)s, `SB` = %(도루)s, `BB` = %(사사구)s, `SO` = %(삼진)s, `AVG` = %(타율)s, `OBA` = %(출루율)s, `SA` = %(장타율)s, `OPS` = %(OPS)s WHERE `No` =%(No)s
                    """

                    curs.execute(query=sql,
                                 args={'경기': season_data['경기'], '타석': season_data['타석'], '타수': season_data['타수'],
                                       '안타': season_data['안타'], '2루타': season_data['2타'], '3루타': season_data['3타'],
                                       '홈런': season_data['홈런'], '타점': season_data['타점'], '득점': season_data['득점'],
                                       '도루': season_data['도루'], '사사구': season_data['사사구'], '삼진': season_data['삼진'],
                                       '타율': season_data['타율'], '출루율': season_data['출루율'], '장타율': season_data['장타율'],
                                       'OPS': season_data['OPS'], 'No': key['key']})

                    tmp.commit()
                    return

        sql = """
                    INSERT INTO `sports`.`season_record` (`G`, `PA`, `AB`, `H`, `2B`, `3B`, `HR`, `RBI`, `R`, `SB`, `BB`, `SO`, `AVG`, `OBA`, `SA`, `OPS` ) VALUES (%(경기)s, %(타석)s, %(타수)s, %(안타)s, %(2루타)s, %(3루타)s, %(홈런)s, %(타점)s, %(득점)s, %(도루)s, %(사사구)s, %(삼진)s, %(타율)s, %(출루율)s, %(장타율)s, %(OPS)s)
                    """

        curs.execute(query=sql,
                     args={'경기': season_data['경기'], '타석': season_data['타석'], '타수': season_data['타수'],
                           '안타': season_data['안타'], '2루타': season_data['2타'], '3루타': season_data['3타'],
                           '홈런': season_data['홈런'], '타점': season_data['타점'], '득점': season_data['득점'],
                           '도루': season_data['도루'], '사사구': season_data['사사구'], '삼진': season_data['삼진'],
                           '타율': season_data['타율'], '출루율': season_data['출루율'], '장타율': season_data['장타율'],
                           'OPS': season_data['OPS']})

        tmp.commit()

    # 일일 기록
    def crawl_daily(self):
        for x in range(1,20):
            titles = self.html.xpath('//*[@id="mArticle"]/div/div[3]/div/div[1]/table/thead/tr/th[{}]'.format(x))
            values = self.html.xpath('//*[@id="mArticle"]/div/div[3]/div/div[1]/table/tbody/tr[1]/td[{}]'.format(x))

            if titles == []:
                return
            else:
                daily_data[titles[0].text] = values[0].text.strip()

    # 일일 기록 DB 삽입
    def db_daily(self):
        print('key:', key['key'])
        if daily_data == {}:
            return
        sql = 'select * from `sports`.`daily_record`'
        curs.execute(sql)
        rows = curs.fetchall()

        if len(rows) == 0:
            sql = """
            INSERT INTO `sports`.`daily_record` (`No`, `Date`, `Opponent`, `PA`, `AB`, `H`, `2B`, `3B`, `HR`, `RBI`, `R`, `SB`, `BB`, `SO`, `AVG`, `OBA`, `SA`, `OPS` ) VALUES (%(No)s, %(날짜)s, %(상대)s, %(타석)s, %(타수)s, %(안타)s, %(2루타)s, %(3루타)s, %(홈런)s, %(타점)s, %(득점)s, %(도루)s, %(사사구)s, %(삼진)s, %(타율)s, %(출루율)s, %(장타율)s, %(OPS)s)
            """

            curs.execute(query=sql,
                         args={'No': key['key'], '날짜': daily_data['날짜'], '상대': daily_data['상대'], '타석': daily_data['타석'], '타수': daily_data['타수'],
                               '안타': daily_data['안타'], '2루타': daily_data['2타'], '3루타': daily_data['3타'],
                               '홈런': daily_data['홈런'], '타점': daily_data['타점'], '득점': daily_data['득점'],
                               '도루': daily_data['도루'], '사사구': daily_data['사사구'], '삼진': daily_data['삼진'],
                               '타율': daily_data['타율'], '출루율': daily_data['출루율'], '장타율': daily_data['장타율'],
                               'OPS': daily_data['OPS']})

            tmp.commit()

            return

        else:
            for x in range(len(rows)):
                if key['key'] == rows[x][0]:
                    sql = """
                    UPDATE `sports`.`daily_record` SET `Date` = %(날짜)s, `Opponent` = %(상대)s, `PA` = %(타석)s, `AB` = %(타수)s, `H` = %(안타)s, `2B` = %(2루타)s, `3B` = %(3루타)s, `HR` = %(홈런)s, `RBI` = %(타점)s, `R` = %(득점)s, `SB` = %(도루)s, `BB` = %(사사구)s, `SO` = %(삼진)s, `AVG` = %(타율)s, `OBA` = %(출루율)s, `SA` = %(장타율)s, `OPS` = %(OPS)s WHERE `No` =%(No)s
                    """
                    curs.execute(query=sql,
                                 args={'날짜': daily_data['날짜'], '상대': daily_data['상대'], '타석': daily_data['타석'], '타수': daily_data['타수'],
                                       '안타': daily_data['안타'], '2루타': daily_data['2타'], '3루타': daily_data['3타'],
                                       '홈런': daily_data['홈런'], '타점': daily_data['타점'], '득점': daily_data['득점'],
                                       '도루': daily_data['도루'], '사사구': daily_data['사사구'], '삼진': daily_data['삼진'],
                                       '타율': daily_data['타율'], '출루율': daily_data['출루율'], '장타율': daily_data['장타율'],
                                       'OPS': daily_data['OPS'], 'No': key['key']})

                    tmp.commit()
                    return

            sql = """
            INSERT INTO `sports`.`daily_record` (`No`, `Date`, `Opponent`, `PA`, `AB`, `H`, `2B`, `3B`, `HR`, `RBI`, `R`, `SB`, `BB`, `SO`, `AVG`, `OBA`, `SA`, `OPS` ) VALUES (%(No)s, %(날짜)s, %(상대)s, %(타석)s, %(타수)s, %(안타)s, %(2루타)s, %(3루타)s, %(홈런)s, %(타점)s, %(득점)s, %(도루)s, %(사사구)s, %(삼진)s, %(타율)s, %(출루율)s, %(장타율)s, %(OPS)s)
            """

            curs.execute(query=sql,
                         args={'No': key['key'], '날짜': daily_data['날짜'], '상대': daily_data['상대'], '타석': daily_data['타석'], '타수': daily_data['타수'],
                               '안타': daily_data['안타'], '2루타': daily_data['2타'], '3루타': daily_data['3타'],
                               '홈런': daily_data['홈런'], '타점': daily_data['타점'], '득점': daily_data['득점'],
                               '도루': daily_data['도루'], '사사구': daily_data['사사구'], '삼진': daily_data['삼진'],
                               '타율': daily_data['타율'], '출루율': daily_data['출루율'], '장타율': daily_data['장타율'],
                               'OPS': daily_data['OPS']})
            tmp.commit()

    # 통산기록
    def crawl_total(self):
        for x in range(3, 19):
            title = self.html2.xpath('//*[@id="mArticle"]/div/div[3]/div/table/thead/tr/th[{}]'.format(x))
            value = self.html2.xpath('//*[@id="mArticle"]/div/div[3]/div/table/tfoot/tr/td[{}]'.format(x))

            total_data[title[0].text] = value[0].text.strip()

    # 통산 기록 DB 삽입
    def db_total(self):
        sql = 'select * from `sports`.`total_record`'
        curs.execute(sql)
        rows = curs.fetchall()

        if len(rows) == 0:
            sql = """
            INSERT INTO `sports`.`total_record` (`G`, `PA`, `AB`, `H`, `2B`, `3B`, `HR`, `RBI`, `R`, `SB`, `BB`, `SO`, `AVG`, `OBA`, `SA`, `OPS` ) VALUES (%(경기)s, %(타석)s, %(타수)s, %(안타)s, %(2루타)s, %(3루타)s, %(홈런)s, %(타점)s, %(득점)s, %(도루)s, %(사사구)s, %(삼진)s, %(타율)s, %(출루율)s, %(장타율)s, %(OPS)s)
            """

            curs.execute(query=sql,
                         args={'경기': total_data['경기'], '타석': total_data['타석'], '타수': total_data['타수'],
                               '안타': total_data['안타'], '2루타': total_data['2타'], '3루타': total_data['3타'],
                               '홈런': total_data['홈런'], '타점': total_data['타점'], '득점': total_data['득점'],
                               '도루': total_data['도루'], '사사구': total_data['사사구'], '삼진': total_data['삼진'],
                               '타율': total_data['타율'], '출루율': total_data['출루율'], '장타율': total_data['장타율'],
                               'OPS': total_data['OPS']})

            tmp.commit()

            return

        else:
            for x in range(len(rows)):
                if key['key'] == rows[x][0]:
                    sql = """
                    UPDATE `sports`.`total_record` SET `G` = %(경기)s, `PA` = %(타석)s, `AB` = %(타수)s, `H` = %(안타)s, `2B` = %(2루타)s, `3B` = %(3루타)s, `HR` = %(홈런)s, `RBI` = %(타점)s, `R` = %(득점)s, `SB` = %(도루)s, `BB` = %(사사구)s, `SO` = %(삼진)s, `AVG` = %(타율)s, `OBA` = %(출루율)s, `SA` = %(장타율)s, `OPS` = %(OPS)s WHERE `No` =%(No)s
                    """

                    curs.execute(query=sql,
                                 args={'경기': total_data['경기'], '타석': total_data['타석'], '타수': total_data['타수'],
                                       '안타': total_data['안타'], '2루타': total_data['2타'], '3루타': total_data['3타'],
                                       '홈런': total_data['홈런'], '타점': total_data['타점'], '득점': total_data['득점'],
                                       '도루': total_data['도루'], '사사구': total_data['사사구'], '삼진': total_data['삼진'],
                                       '타율': total_data['타율'], '출루율': total_data['출루율'], '장타율': total_data['장타율'],
                                       'OPS': total_data['OPS'], 'No': key['key']})

                    tmp.commit()
                    return

        sql = """
        INSERT INTO `sports`.`total_record` (`G`, `PA`, `AB`, `H`, `2B`, `3B`, `HR`, `RBI`, `R`, `SB`, `BB`, `SO`, `AVG`, `OBA`, `SA`, `OPS` ) VALUES (%(경기)s, %(타석)s, %(타수)s, %(안타)s, %(2루타)s, %(3루타)s, %(홈런)s, %(타점)s, %(득점)s, %(도루)s, %(사사구)s, %(삼진)s, %(타율)s, %(출루율)s, %(장타율)s, %(OPS)s)
        """

        curs.execute(query=sql,
                     args={'경기': total_data['경기'], '타석': total_data['타석'], '타수': total_data['타수'], '안타': total_data['안타'],
                           '2루타': total_data['2타'], '3루타': total_data['3타'], '홈런': total_data['홈런'], '타점': total_data['타점'],
                           '득점': total_data['득점'], '도루': total_data['도루'], '사사구': total_data['사사구'], '삼진': total_data['삼진'],
                           '타율': total_data['타율'], '출루율': total_data['출루율'], '장타율': total_data['장타율'],
                           'OPS': total_data['OPS']})

        tmp.commit()

    # 선수 프로필 사진
    def crawl_img(self):
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

    #선수 스탯 계산
    def cal_stat(self):
        sb = []
        eye = []

        sb_and_eye = sb_eye(sb, eye)

        sql = 'select * from `sports`.`total_record` where No = %(번호)s'
        curs.execute(query=sql, args={'번호':key['key']})
        rows = curs.fetchall()

        stat['contact'] = (round(rows[0][13] * 312.5))
        stat['power'] = (round(rows[0][15] * 10000 / 52))
        stat['speed'] = sb_and_eye[0][key['key']-1]
        stat['eye'] = round(sb_and_eye[1][key['key']-1] * 100)


    def db_stat(self):
        sql = 'select * from `sports`.`stat` where No = %(번호)s'
        curs.execute(query=sql, args={'번호':key['key']})
        rows = curs.fetchall()

        if len(rows) == 0:
            print('add')
            sql = """
                insert into `sports`.`stat` (`Contact`, `Power`, `Speed`, `Eye`)
                values (%(컨택)s, %(파워)s, %(스피드)s, %(선구안)s)
                """
            curs.execute(query=sql,
                         args={'컨택': stat['contact'], '파워': stat['power'], '스피드': stat['speed'], '선구안': stat['eye']})

        else:
            sql = """
                update `sports`.`stat` set `Contact` = %(컨택)s, `Power` = %(파워)s, `Speed` = %(스피드)s, `Eye` = %(선구안)s
                where No = %(번호)s
                """
            curs.execute(query=sql, args={'컨택':stat['contact'],'파워': stat['power'], '스피드':stat['speed'], '선구안':stat['eye'], '번호':key['key']})

        tmp.commit()

def sb_eye(list1, list2):
    sb = []
    eye = []

    sql = 'select sb, g, bb, so from `sports`.`total_record`'
    curs.execute(query=sql)
    t_row = curs.fetchall()

    for x in range(len(t_row)):
        sb.append(round(t_row[x][0] / t_row[x][1] * 144 * 3))

        if sb[x] >= 70 and sb[x] < 80:
            sb[x] += 3

        elif sb[x] >= 60 and sb[x] < 70:
            sb[x] += 10

        elif sb[x] >= 50 and sb[x] < 60:
            sb[x] += 18

        elif sb[x] >= 40 and sb[x] < 50:
            sb[x] += 23

        elif sb[x] >= 30 and sb[x] < 40:
            sb[x] += 28

        elif sb[x] >= 20 and sb[x] < 30:
            sb[x] += 33

        elif sb[x] >= 10 and sb[x] < 20:
            sb[x] += 43

        elif sb[x] >= 5 and sb[x] < 10:
            sb[x] += 48
        elif sb[x] <= 5:
            sb[x] += 50

    for x in range(len(t_row)):
        eye.append(t_row[x][2] / t_row[x][3])
        if eye[x] >= 0.6 and eye[x] <= 0.7:
            eye[x] += 0.3

        if eye[x] >= 0.5 and eye[x] <= 0.6:
            eye[x] += 0.7

        elif eye[x] >= 0.4 and eye[x] < 0.5:
            eye[x] += 0.10

        elif eye[x] >= 0.3 and eye[x] < 0.4:
            eye[x] += 0.20

        elif eye[x] >= 0.2 and eye[x] < 0.3:
            eye[x] += 0.29

        elif eye[x] >= 0.1 and eye[x] < 0.2:
            eye[x] += 0.39

        elif eye[x] >= 0.1 and eye[x] < 0.0:
            eye[x] += 0.50


    list1 = sb
    list2 = eye

    return list1, list2

if __name__ == '__main__':
    sbna = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=778542',
          'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=778542']

    mwpark = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=778528',
            'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=778528']

    yklee = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=10018',
           'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=10018']

    wskim = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=433981',
           'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=433981']

    dhlee = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=9889',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=9889']

    tkkim = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=9898',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=9898']

    mhkang = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=10036',
              'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=10036']

    asson = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=10254',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=10254']

    sylee = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=434006',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=434006']

    hipark = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=9882',
              'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=9882']

    rosario = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=1216230',
               'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=1216230']

    gwjeong = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=10119',
               'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=10119']

    gmsong = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=10196',
              'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=10196']

    jhchoi = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=10315',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=10315']

    jchoi = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=10121',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=10121']

    gcseo = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=10722',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=10722']

    bhmin = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=10137',
             'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=10137']

    jsha = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=433972',
            'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=433972']

    hmpark = ['http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_main.daum?person_id=435395',
              'http://score.sports.media.daum.net/record/baseball/kbo/plrinf_bat_rechist.daum?person_id=435395']

    player = [sbna,mwpark,yklee,wskim,dhlee, tkkim, mhkang, asson, gcseo, jchoi, jhchoi, gmsong, gwjeong, rosario,
              hipark, sylee, bhmin, jsha, hmpark]

    test = [yklee]
    for x in player:
        a = basic(x)

        a.crawl_profile()
        a.crawl_daily()
        a.crawl_season()
        a.crawl_total()
        a.crawl_img()


        a.db_profile()
        a.db_daily()
        a.db_season()
        a.db_total()

        a.cal_stat()
        a.db_stat()