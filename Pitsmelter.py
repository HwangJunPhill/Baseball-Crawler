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
            SELECT * FROM `pitseason_record` WHERE `No` = %(번호)s
            """
        curs.execute(query=sql, args={'번호':number})
        rows = curs.fetchall()

        sql = """
            SELECT `Name` FROM `pitprofile` WHERE `No` = %(번호)s
            """
        curs.execute(query=sql, args={'번호':number})
        name = curs.fetchall()

        print(name)
        stat['name'] = name[0][0]

        curec['g'] = rows[0][1]
        curec['leftgame'] = 144 * curec['g']/self.getleftgame()
        curec['w'] = rows[0][2]
        curec['l'] = rows[0][3]
        curec['s'] = rows[0][4]
        curec['h'] = rows[0][5]
        curec['ip'] = rows[0][6]
        curec['k'] = rows[0][10]
        curec['er'] = rows[0][13]
        curec['qs'] = rows[0][16]

        if '/' in curec['ip']:
            i = int(curec['ip'][:len(curec['ip'])-3])
            j = int(curec['ip'][-3])
            curec['ip']=(i + j / 3)

        else:
            curec['ip'] = int(curec['ip'])


    def getleftgame(self):
        gamesum = 0
        for x in range(1, 11):
            nowgame = self.html.xpath('//*[@id="table1"]/tbody/tr[{}]/td[3]'.format(x))
            gamesum += (int(nowgame[0].text))

        return round(gamesum/10)
 
    def calculate(self):

        stat['leftgame'] = curec['leftgame'] + curec['g']
        stat['w'] = round(curec['leftgame'] * (curec['w'] / curec['g']) + curec['w'])
        stat['l'] = round(curec['leftgame'] * (curec['l'] / curec['g']) + curec['l'])
        stat['s'] = round(curec['leftgame'] * (curec['s'] / curec['g']) + curec['s'])
        stat['h'] = round(curec['leftgame'] * (curec['h'] / curec['g']) + curec['h'])
        stat['ip'] = round(curec['leftgame'] * (curec['ip'] / curec['g']) + curec['ip'])
        stat['k'] = round((curec['leftgame'] * (curec['k'] / curec['g']) + curec['k']))
        stat['era'] = round((curec['leftgame'] * (curec['er'] / curec['g'])) * 9 / stat['ip'],2)
        stat['qs'] = round(curec['leftgame'] * curec['qs']/curec['g'])

    def db_smelt(self):
        sql = 'select * from `sports`.`pitsmelt` where name = %(이름)s'
        curs.execute(query=sql, args={'이름':stat['name']})
        rows = curs.fetchall()

        if len(rows) == 0:
            print('add')
            sql = 'INSERT INTO `sports`.`pitsmelt` (`name`) VALUES (%(이름)s)'
            curs.execute(query=sql,
                         args={'이름': stat['name']})
            tmp.commit()


        sql = """
        UPDATE `sports`.`pitsmelt` SET `leftgame` = %(잔여경기)s, `w` = %(승)s,
        `l` = %(패)s,  `s` = %(세)s, `h` = %(홀)s, `ip` = %(이닝)s, `k` = %(탈삼진)s, `era` = %(평자)s, `qs` = %(qs)s
        where `name` = %(이름)s
        """

        curs.execute(query=sql,
                     args={'잔여경기': stat['leftgame'], '승': stat['w'], '패': stat['l'],
                           '세': stat['s'], '홀': stat['h'], '이닝': stat['ip'],
                           '탈삼진': stat['k'], '평자':stat['era'], 'qs': stat['qs'], '이름':stat['name']})

        tmp.commit()


if __name__ == '__main__':
    smt = smelt()
    sql = """
        SELECT `No` FROM `pitprofile`
        """
    curs.execute(query=sql)
    rows = curs.fetchall()


    for x in range(1,len(rows)+1):
        smt.get(x)
        smt.calculate()
        smt.db_smelt()