import pymysql

tmp = pymysql.connect(host='localhost', user='root', password='', db='sports', charset='utf8')
curs = tmp.cursor()

sql = 'select * from `sports`.`season_record`'
curs.execute(sql)
rows = curs.fetchall()

sql = """
    SELECT * FROM `season_record` WHERE `No` = 5
    """

curs.execute(query=sql)

rows = curs.fetchall()

leftgame = 0
g = rows[0][1]
h = rows[0][4]
hr = rows[0][7]
avg = rows[0][4]
rbi = rows[0][8]
sb = rows[0][10]

print('남은 출장 기회 : ', 144-g)
print('에상 안타 수 : ',round((144-g)*(h/g)+h))
print('예상 홈런 수',round((144-g)*(hr/g)+hr))
print('예상 타율', round(((144-g)*(h/g)+h)/((144-rows[0][1])*(rows[0][2]/g)+rows[0][2]),3))
print('예상 타점', round((144-g)*(rbi/g)+rbi))
print('예상 도루',round(sb/g * (144-g) + sb))

#print(rows[0])