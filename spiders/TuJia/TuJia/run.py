# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/3/28 21:09
# File : run.py


from scrapy.cmdline import execute

if __name__ == '__main__':
    execute('scrapy crawl Tujia_spider'.split())