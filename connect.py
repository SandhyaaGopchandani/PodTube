import configparser
#import MYSQLdb.cursors
import pymysql
import pymysql.cursors

config = configparser.ConfigParser()
config.read('config.ini')

def connect2db():
        charset='utf8mb4'
        host='podtube-db.cfdu4kcak0c0.us-east-2.rds.amazonaws.com'
        user='podtube'
        password='admin12345'
        db=''
        port=3306
        conn = pymysql.connect(charset=charset, host=host,user=user,passwd=password,db=db, port=port)
        #db  = pymysql.connect(host=config['mysqlDB']['host'],
        #        charset='utf8mb4',
        #        user=config['mysqlDB']['user'],
        #         port=config['mysqlDB']['port'],
        #        passwd=config['mysqlDB']['password'],
        #       db=config['mysqlDB']['dbname'])
        #conn = pymysql.connect(host, user=user,port=port, passwd=password, db=dbname)

        return conn


