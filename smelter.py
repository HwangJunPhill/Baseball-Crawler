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

    def get(self, number=1):
        sql = """
            SELECT * FROM `season_record` WHERE `No` = %(번호)s
            """
        curs.execute(query=sql, args={'번호':number})
        rows = curs.fetchall()

        sql = """
            SELECT `Name` FROM `profile` WHERE `No` = %(번호)s
            """
        curs.execute(query=sql, args={'번호':number})
        name = curs.fetchall()

        print(name)
        stat['name'] = name[0][0]

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

    def db_smelt(self):
        sql = 'select * from `sports`.`smelt` where name = %(이름)s'
        curs.execute(query=sql, args={'이름':stat['name']})
        rows = curs.fetchall()

        if len(rows) == 0:
            print('add')
            sql = 'INSERT INTO `sports`.`smelt` (`name`) VALUES (%(이름)s)'
            curs.execute(query=sql,
                         args={'이름': stat['name']})
            tmp.commit()


        sql = """
        UPDATE `sports`.`smelt` SET `leftgame` = %(잔여경기)s, `h` = %(안타)s,
        `hr` = %(홈런)s,  `avg` = %(타율)s, `rbi` = %(타점)s, `sb` = %(도루)s where `name` = %(이름)s
        """

        curs.execute(query=sql,
                     args={'잔여경기': stat['leftgame'], '안타': stat['h'], '홈런': stat['hr'],
                           '타율': stat['avg'], '타점': stat['rbi'], '도루': stat['sb'], '이름':stat['name']})

        tmp.commit()


if __name__ == '__main__':
    smt = smelt()
    for x in range(1,18):
        smt.get(x)
        smt.calculate()
        smt.db_smelt()