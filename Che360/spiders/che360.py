import ujson
from scrapy import Spider
from scrapy.http import FormRequest, Request
from ..items import Che360Item, Che360URLItem
from bs4 import BeautifulSoup
from Che360.spiders.extractors import get_page_num, gen_post, gen_post_page, gen_item
import pprint

pp = pprint.PrettyPrinter(indent=4, width=180)


class CheJiyouSpider(Spider):
    name = 'chejiyousipder'
    allowed_domains = ['bbs.360che.com']

    def __init__(self, *, url_jiyou, type_):
        super(CheJiyouSpider).__init__()
        self.url_jiyou = url_jiyou
        self.type_ = type_

    def start_requests(self):
        yield Request(url='https://bbs.360che.com/{}-{}-1.html'.format(self.type_, self.url_jiyou),
                      callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        yield from (
            Request(
                url='https://bbs.360che.com/{type_}-{club}-{page}.html'.format(
                    type_=self.type_,
                    club=self.url_jiyou,
                    page=x),
                callback=self.parse_page)
            for x in range(2, get_page_num(soup)))

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # print('ok')
        yield from (Request(url='https://bbs.360che.com/{}'.format(post_url),
                            callback=self.parse_post,
                            meta={'initial': 1, 'refer_page': response.url})
                    for post_url in gen_post(soup))

    def parse_post(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        post_id = response.url.split('-')[1]
        yield Che360URLItem(refer_page=response.meta['refer_page'], post_id=post_id, url=response.url)
        if response.meta['initial'] and gen_post_page(soup, response.url):
            yield from (Request(
                url=href,
                callback=self.parse_post,
                meta={'initial': 0, 'refer_page': response.url}
            ) for href in gen_post_page(soup, response.url))

        yield from(Che360Item(
            post_id=post_id,
            url=response.url,
            sequence=item['sequence'],
            user_id=item['user_id'],
            user_registtime=item['regstime'],
            user_postnum=item['postnum'],
            user_location=item['location'],
            created_time=item['created_time'],
            content=item['content'],
            num_reply=item['num_reply'],
            title=item['title']
        ) for item in gen_item(soup) if item)

        # for item in gen_item(soup):
        #     if item:
        #         yield Che360Item(
        #             post_id=post_id,
        #             url=response.url,
        #             sequence=item['sequence'],
        #             user_id=item['user_id'],
        #             user_registtime=item['regstime'],
        #             user_postnum=item['postnum'],
        #             user_location=item['location'],
        #             created_time=item['created_time'],
        #             content=item['content'],
        #             num_reply=item['num_reply'],
        #             title=item['title'])


if __name__ == '__main__':
    pass
