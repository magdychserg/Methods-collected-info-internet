from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from shopparser.shopparser import settings
from shopparser.shopparser.spiders.castorama import CastoramalinruSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(CastoramalinruSpider)

    process.start()