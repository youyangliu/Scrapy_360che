# Scrapy_360che
using scrapy &amp; beautifulsoup to crawl the website

Just run the run_spider_jiyouluntan.py file and you will crawl the club and save the results to local automatically. Change the url_jiyou number if you want to change another website. Change the local path that you save the file.

The data structures are defined in item.py file

class Che360Item(Item):
    url = Field()
    post_id = Field()
    sequence = Field()
    user_id = Field()
    user_registtime= Field()
    user_postnum = Field()
    user_location = Field()
    created_time = Field()
    content = Field()
    num_reply = Field()
    title = Field()
class Che360URLItem(Item):
    url = Field()
    post_id= Field()
    refer_page = Field()
