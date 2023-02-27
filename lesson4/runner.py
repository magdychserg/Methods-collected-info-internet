from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lesson4.hhparse import settings
from lesson4.hhparse.spider.hh import HhSpider #паук для Урок 4

if __name__ == '__main__':
    scr_settings = Settings()
    scr_settings.setmodule(settings)
    process = CrawlerProcess(settings=scr_settings)
    process.crawl(HhSpider)  # задаем паука из ДЗ к Урок 4
    process.start()
