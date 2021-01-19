# -*- codeing = utf-8 -*-
# @Time : 2021/1/11 11:23
# @Author : jzy
# @File : sql.py
# @Software : PyCharm
import pymysql
import csv
import codecs

con = pymysql.connect(
    host='localhost',
    user='root',
    passwd='123456',
    database='qixin',
    port=3306,
    charset='utf8')
cur = con.cursor()
sql = """
CREATE TABLE qixin_data (
number VARCHAR(20),
law_date  VARCHAR(20) ,
reason VARCHAR(20),
identity VARCHAR(20),
content VARCHAR(255)
)ENGINE=innodb DEFAULT CHARSET=utf8;
"""
cur.execute(sql)


with codecs.open(filename='./qixin_data.csv', mode='r', encoding='gbk') as f:
    reader = csv.reader(f)
    Insert_sql = 'insert into qixin_data values(%s,%s,%s,%s,%s)'
    for item in reader:
        args = tuple(item)
        cur.execute(Insert_sql,args)

con.commit()
cur.close()
con.close()