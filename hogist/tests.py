import psycopg2
from django.test import TestCase

# # Create your tests here.
# def DbConnect(query):
#     conn = psycopg2.connect(
#         host="ls-0438f08a704227d445cfa8ff64e4f7df8e84bb1e.cu81vx4tdqjc.ap-south-1.rds.amazonaws.com",
#         database="dbaimaster", port=5432, user='dbmasteruser', password='a+5[8ql+{frL>S!gO).QFrxjxor:;B>u')
#     curr = conn.cursor()
#     print("Connect ", curr)
#     curr.execute(query)
#
#     rows = curr.fetchall()[0]
#     print("ROWS", rows)
#     print("GYPE", type(rows[1]))
#     return rows


# DbConnect('SELECT * FROM user_ipdetails ORDER BY id desc ;').

conn = psycopg2.connect(
    host="ls-0438f08a704227d445cfa8ff64e4f7df8e84bb1e.cu81vx4tdqjc.ap-south-1.rds.amazonaws.com",
    database="dbaimaster", port=5432, user='dbmasteruser', password='a+5[8ql+{frL>S!gO).QFrxjxor:;B>u')
curr = conn.cursor()
query = """ SELECT * FROM user_ipdetails ORDER BY id desc """
curr.execute(query)
rows = curr.fetchall()

import datetime
# from django.utils import timezone
import pytz
today = datetime.datetime.now(datetime.timezone.utc).replace(hour=0,minute=0,second=0,microsecond=0)
# today = datetime.datetime.combine(today,datetime.datetime.min.time())
# r = today.replace(tzinfo=pytz.utc)
print('TOFAY,', today)
last_monday = today - datetime.timedelta(days=today.weekday())
# l = last_monday.replace(tzinfo=pytz.utc)
print('LAST MONDAY', last_monday)

for i in rows:
    t = i[5]
    if t > last_monday:
        print("tume", t)

# import calendar
#
# d = dict(enumerate(calendar.day_name))
# print(d)
