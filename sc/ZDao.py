#coding:utf-8
import pymysql
def getConnect():
    db = pymysql.connect(
        host='localhost',
        port=3306,
        database='xm',
        user='root',
        passwd='root',
        charset='utf8'
    )
    return db;