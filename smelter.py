import requests
from lxml import etree
import pymysql

tmp = pymysql.connect(host='localhost', user='root', password='', db='sports', charset='utf8')
curs = tmp.cursor()

curec = {}
stat = {}
key = {}

class smelt():

    def __init__(self):
        self.url = 'http://score.sports.media.daum.net/record/baseball/kbo/trnk.daum'
        self.respose = requests.get(self.url)
        self.html = etree.HTML(self.respose.text)

        self.get()

    def get(self):
        sql = """
            SELECT * FROM `season_record` WHERE `No` = 1
            """
        curs.execute(query=sql)
        rows = curs.fetchall()

        sql = """
            SELECT `Name` FROM `profile` WHERE `No` = 1
            """
        curs.execute(query=sql)
        name = curs.fetchall()

        print(name[0][0])
        stat['name'] = name[0][0]

        #딕셔너리에 넣고 알아서 척척
        #예측 하기

        curec['leftgame'] = 144 - self.getleftgame()
        curec['g'] = rows[0][1]
        curec['ab'] = rows[0][2]
        curec['h'] = rows[0][4]
        curec['hr'] = rows[0][7]
        curec['avg'] = rows[0][4]
        curec['rbi'] = rows[0][8]
        curec['sb'] = rows[0][10]

    def getleftgame(self):
        gamesum = 0
        for x in range(1, 11):
            nowgame = self.html.xpath('//*[@id="table1"]/tbody/tr[{}]/td[3]'.format(x))
            gamesum += (int(nowgame[0].text))

        return round(gamesum/10)


    def calculate(self):

        stat['leftgame'] = curec['leftgame']
        stat['h'] = round(curec['leftgame'] * (curec['h'] / curec['g']) + curec['h'])
        stat['hr'] = round(curec['leftgame'] * (curec['hr'] / curec['g']) + curec['hr'])
        stat['avg'] = round((curec['leftgame'] * (curec['h'] / curec['g']) + curec['h']) / (curec['leftgame'] * (curec['ab'] / curec['g']) + curec['ab']), 3)
        stat['rbi'] = round(curec['leftgame'] * (curec['rbi'] / curec['g']) + curec['rbi'])
        stat['sb'] = round(curec['sb'] / curec['g'] * curec['leftgame'] + curec['sb'])

        # print('남은 출장 기회 : ', curec['leftgame'])
        # print('에상 안타 수 : ', round(curec['leftgame'] * (curec['h'] / curec['g']) + curec['h']))
        # print('예상 홈런 수', round(curec['leftgame'] * (curec['hr'] / curec['g']) + curec['hr']))
        # print('예상 타율', round((curec['leftgame'] * (curec['h'] / curec['g']) + curec['h']) / (curec['leftgame'] * (curec['ab'] / curec['g']) + curec['ab']), 3))
        # print('예상 타점', round(curec['leftgame'] * (curec['rbi'] / curec['g']) + curec['rbi']))
        # print('예상 도루', round(curec['sb'] / curec['g'] * curec['leftgame'] + curec['sb']))


    def db_smelt(self):
        sql = 'select * from `sports`.`smelt`'
        curs.execute(sql)
        rows = curs.fetchall()

        if len(rows) == 0:
            print('lets go')
            sql = """
                    INSERT INTO `sports`.`smelt` (`leftgame`, `name`, `h`, `hr`, `avg`, `rbi`, `sb`) VALUES (%(잔여경기)s, %(이름)s, %(안타)s, %(홈런)s, %(타율)s, %(타점)s, %(도루)s)
                    """

            curs.execute(query=sql,
                         args={'잔여경기': stat['leftgame'], '이름': stat['name'], '안타':stat['h'], '홈런':stat['hr'], '타율':stat['avg'], '타점':['rbi'], '도루':['sb']})
            tmp.commit()
            return

        else:
            for x in range(len(rows)):
                    sql = """
                    UPDATE `sports`.`smelt` SET `leftgame` = %(잔여경기)s, `name` = %(이름)s, `h` = %(안타)s, `hr` = %(홈런)s, `avg` = %(타율)s
                    """

                    curs.execute(query=sql,
                                 args={'잔여경기': stat['leftgame'], '이름': stat['name'], '안타': stat['h'], '홈런': stat['hr'], '타율':stat['avg']})

                    tmp.commit()
                    return

        sql = """
                INSERT INTO `sports`.`smelt` (`leftgame`, `name`, `h`, `hr`, `avg`, `rbi`, `sb`) VALUES (%(잔여경기)s, %(이름)s, %(안타)s, %(홈런)s, %(타율)s, %(타점)s, %(도루)s)
                """

        curs.execute(query=sql,
                     args={'잔여경기': stat['leftgame'], '이름': stat['name'], '안타': stat['h'], '홈런': stat['hr'], '타율': stat['avg'],
                           '타점': ['rbi'], '도루': ['sb']})
        tmp.commit()

if __name__ == '__main__':
    a = smelt()
    a.calculate()
    a.db_smelt()