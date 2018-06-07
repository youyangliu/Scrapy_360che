from scrapy import Item
from scrapy import Field


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
