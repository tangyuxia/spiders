# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TujiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    region = scrapy.Field()  # 地区
    hotel_name = scrapy.Field()  # 酒店名称
    price = scrapy.Field()  # 价格
    room_type = scrapy.Field()  # 房型号
    unit_id=scrapy.Field()
