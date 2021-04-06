import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import EequitybankItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class NewsSpider(scrapy.Spider):
    name = 'news'
    start_urls = ['https://www.equitybank.com/connect/news-and-events']

    def parse(self, response):
        post_links = response.xpath(
            '//a[contains(text(),"Read")]/@href').getall()
        yield from response.follow_all(post_links, self.parse_post)

    def parse_post(self, response):
        date = "Not in article"
        title = response.xpath('//div[@data-content="content"]/h2/text()').get()
        content = response.xpath('//div[@class="content"]//text()').getall()
        content = [p.strip() for p in content if p.strip()]
        content = re.sub(pattern, "", ' '.join(content))

        item = ItemLoader(item=EequitybankItem(), response=response)
        item.default_output_processor = TakeFirst()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)
        item.add_value('date', date)

        yield item.load_item()
