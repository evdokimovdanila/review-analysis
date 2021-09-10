import time
import scrapy
from urllib.parse import urljoin
from irecommend.items import IrecommendItem


class IrecommendPhones(scrapy.Spider):
    name = 'irecommend_phones'
    allowed_domains = ['https://irecommend.ru']
    start_urls = ['https://irecommend.ru/srch?page=1&query=телефоны']

    visited_urls = []
    start_page = "1"

    def parse(self, response):
        print(response.url)
        if response.url not in self.visited_urls:
            self.visited_urls.append(response.url)
            urls_phones = response.xpath('//div[@class="title"]/a/@href').extract()
            for cur_url_phone in urls_phones:
                url_phone = urljoin(response.url, cur_url_phone)
                yield response.follow(url_phone, callback=self.parse_phone, dont_filter=True)

            number_next_page = response.xpath('//li[contains(@class,"pager-current")]/text()').extract()
            next_page_url = response.url.replace(self.start_page, number_next_page[0], 1)
            self.start_page = number_next_page[0]
            yield response.follow(next_page_url, callback=self.parse, dont_filter=True)

    def parse_phone(self, response):
        print(response.url)
        type_item = response.xpath('//div[@class="voc-group vid-1"]/a/text()').extract()
        if type_item[0] == "Мобильные телефоны":
            print(type_item[0])
            reviews_link = response.xpath('//div[@class="reviewTitle"]/a/@href').extract()
            for curr_review_link in reviews_link:
                review_url = urljoin(response.url, curr_review_link)
                yield response.follow(review_url, callback=self.parse_review, dont_filter=True)

    def parse_review(self, response):
        print(response.url)
        item = IrecommendItem()
        text = response.xpath('//div[@class="description hasinlineimage"]/p').extract()
        item['text'] = text
        label = response.xpath('//span[@class="verdict"]/text()').extract()
        item['label'] = label[0]
        print('Review sent')
        yield item

