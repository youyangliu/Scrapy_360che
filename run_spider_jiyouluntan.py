from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from Che360.spiders.che360 import CheJiyouSpider

if __name__ == '__main__':
    url_jiyou = '759'  # 机油论坛编号
    type_ = 'club'  # 机油论坛类型
    settings = get_project_settings()
    settings.update({'LOG_LEVEL': 'INFO'})
    settings.update({'JSON_FILE_PATH':
                         '/Users/youyang/PycharmProjects/Che_Processing/raw_data/jiyouluntan_comments.json',
                     'URL_FILE_PATH': '/Users/youyang/PycharmProjects/Che_Processing/raw_data/jiyouluntan_url.json'})
    process = CrawlerProcess(settings)
    process.crawl(CheJiyouSpider, url_jiyou=url_jiyou, type_=type_)
    process.start()
