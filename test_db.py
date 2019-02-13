import pymysql

connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                             user='cs4400_group6',
                             password='z4GciftG',
                             db='cs4400_group6')

if connection.open:
    print("it works!!")