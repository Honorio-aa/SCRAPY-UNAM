import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from unam.items import UnamItem

class UnamSpider(CrawlSpider):
    name = 'unam'
    item_count=0
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/page/1/']

    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths= ('//ul/li[@class="next"]/a'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="quote"]/span/a')),
        callback = 'parse_item', follow =False)
    }
    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        
        item=UnamItem()
        item['autor'] = response.xpath('/html/body/div/div[2]/h3/text()').extract()
        item['descripcion'] = response.xpath('/html/body/div/div[2]/div/text()').extract()
        self.item_count+=1
        if self.item_count >= 5:
            raise CloseSpider('item_exceeded')
        yield item
