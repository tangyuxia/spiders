import os

# Scrapy settings for TuJia project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html


DIRNAME = os.path.dirname(os.path.abspath(__file__))
SPIDERS_DIR = os.path.join(DIRNAME, 'spiders')
# js文件的地址
JS_PATH = os.path.join(SPIDERS_DIR, 'fas_session_id.js')

BOT_NAME = "TuJia"
SPIDER_MODULES = ["TuJia.spiders"]
NEWSPIDER_MODULE = "TuJia.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

LOG_LEVEL = 'WARNING'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "TuJia.middlewares.TujiaSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # "TuJia.middlewares.TujiaDownloaderMiddleware": 543,
   "TuJia.middlewares.CookieMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # "TuJia.pipelines.TujiaPipeline": 300,
    "TuJia.pipelines.MySqlPipeline": 400,
    # 使用redis管道，自动存入redis
    'scrapy_redis.pipelines.RedisPipeline': 500

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# 数据库
MYSQL = {
    'host': '127.0.0.1',
    # 'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'db': 'kaohe',
    'table': 'tujia',
    'port': 3306
}

# scrapy-redis 配置
# 使用scrapy_redis调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 直接在 `settings.py` 里面配置为 `REDIS_URL`
# redis://[:password]@host:port/db
# REDIS_URL = 'redis://172.0.0.1:6379/0'

REDIS_HOST = '127.0.0.1'  # 修改为Redis的实际IP地址
REDIS_PORT = 6379  # 修改为Redis的实际端口
REDIS_PARAMS = {
    'db': 1  # 连接哪一个库
}
# 此项配置是可选的，默认使用 `PriorityQueue`。如果想要更改配置，可以配置 SCHEDULER_QUEUE_CLASS 变量
# SCHEDULER_PERSIST = True   # 底层 就是监听爬虫信号  触发redis指令 清空数据库
# 是否允许暂停
SCHEDULER_PERSIST = True

# 此配置是可选的，默认是 False。如果配置了持久化或者强制中断了爬虫，那么爬取队列和指纹集合不会被清空，爬虫重新启动之后就会接着上次爬取。如果想重新爬取，我们可以配置重爬的选项
# SCHEDULER_FLUSH_ON_START = True


