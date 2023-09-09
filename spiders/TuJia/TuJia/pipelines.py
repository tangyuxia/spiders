# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import time

import pymysql
import redis
from scrapy.utils.project import get_project_settings

setting = get_project_settings()
MYSQL = setting['MYSQL']

MYSQL_HOST = MYSQL['host']
MYSQL_USER = MYSQL['user']
MYSQL_PWD = MYSQL['password']
MYSQL_DB = MYSQL['db']
MYSQL_TABLE = MYSQL['table']
MYSQL_PORT = MYSQL['port']


class TujiaPipeline:
    def process_item(self, item, spider):
        print(item)
        time.sleep(1000)
        return item


class MySqlPipeline():
    """mysql存储数据"""

    def open_spider(self, spider_name):
        """打开mysql时候的操作"""
        self.coon = pymysql.Connection(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PWD,
                                       database=MYSQL_DB, charset='utf8')
        # self.coon = pymysql.Connection(host='localhost', port=3306, user='root',password='123456', database='kaohe')

    def process_item(self, item, spider):
        print(item)
        region = item['region']
        hotel_name = item['hotel_name']
        price = item['price']
        room_type = item['room_type']
        unit_id = item['unit_id']

        # 创建sql语句
        select_sql = """select unit_id from %s""" % MYSQL_TABLE

        cursor = self.coon.cursor()
        cursor.execute(select_sql)
        rest = cursor.fetchone()
        print(rest)
        if str(rest[0]) == str(unit_id) or rest:
            # 判断是否有相同的数据，如果有跳过，如果数据库是空的也跳过
            print(rest[0])
            return item
        else:
            # 创建sql语句
            sql = """insert into %s(region,hotel_name,price,room_type,unit_id) values ("%s","%s","%s","%s",%s)""" % (
                MYSQL_TABLE, region, hotel_name, price, room_type, unit_id)
            # print(sql)
            # 创建游标
            sur = self.coon.cursor()
            # 执行sql语句
            sur.execute(sql)
            # 提交
            self.coon.commit()

            return item

    def close_spider(self, spider_name):
        # 关闭数据库连接
        self.coon.close()

# class RedisPipeline:
#     """redis存储数据"""
#
#     def open_spider(self, spider_name):
#         self.coon = redis.Redis(db=1, decode_responses=True)
#
#     def process_item(self, item, spider):
#         return item
#
#     def close_spider(self, spider_name):
#         self.coon.close()
