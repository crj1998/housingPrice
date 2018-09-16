import pymysql
from myScrapy import settings

MYSQL_HOSTS=settings.MYSQL_HOSTS
MYSQL_USER=settings.MYSQL_USER
MYSQL_PASSWORD=settings.MYSQL_PASSWORD
MYSQL_PORT=settings.MYSQL_PORT
MYSQL_DB=settings.MYSQL_DB


cnx=pymysql.connect(host=MYSQL_HOSTS,port=MYSQL_PORT,user=MYSQL_USER,passwd=MYSQL_PASSWORD,db=MYSQL_DB,charset='utf8')
cur=cnx.cursor()

class MySQL:
    @classmethod
    def insertContent(cls,city_name,city_price,year):
        order = "INSERT INTO `housingprice` (`Name`) VALUES ('%s')"%city_name
        cur.execute(order)
        order=''
        for m in city_price:
            order += "`%s.%s`=%s,"%(year,m,city_price[m])
        order = "UPDATE `housingprice` SET "+order[:-1]+" WHERE `Name`='%s'"%city_name
        cur.execute(order)
        cur.connection.commit()

    @classmethod
    def isExist(cls,city_name):
        order = "SELECT EXISTS (SELECT 1 FROM `housingprice` WHERE `Name`='%s')"%city_name
        cur.execute(order)
        return cur.fetchall()[0]

    @classmethod
    def updateContent(cls,city_name,city_price,year):
        order=''
        for m in city_price:
            order += "`%s.%s`=%s,"%(year,m,city_price[m])
        order = "UPDATE `housingprice` SET "+order[:-1]+" WHERE `Name`='%s'"%city_name
        cur.execute(order)
        cur.connection.commit()