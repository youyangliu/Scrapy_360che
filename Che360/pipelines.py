import ujson
from Che360.items import Che360URLItem, Che360Item


# from pymongo import MongoClient


# class MongoPipeline(object):
#     def __init__(self, mongo_uri, mongo_db, mongo_coll):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#         self.mongo_coll = mongo_coll
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         settings = crawler.settings
#         return cls(
#             mongo_uri=settings.get('MONGO_URI'),
#             mongo_db=settings.get('MONGO_DATABASE', 'weibo'),
#             mongo_coll=settings.get('MONGO_COLLECTION', 'result')
#         )
#
#     def open_spider(self, spider):
#         self.client = MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#         self.coll = self.db[self.mongo_coll]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         result = dict(item)
#         self.coll.update_one(
#             {'_id': result['idstr']},
#             {'$set': result['mblog']},
#             upsert=True
#         )
#         return item


class JsonWriterPipeline(object):
    def __init__(self, file_path, url_path):
        self.file_path = file_path
        self.url_path = url_path

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            file_path=settings.get('JSON_FILE_PATH', 'items.jl'),
            url_path=settings.get('URL_FILE_PATH', 'items.jl')
        )

    def open_spider(self, spider):
        self.file = open(self.file_path, 'a+')
        self.url_file = open(self.url_path, 'a+')

    def close_spider(self, spider):
        self.file.close()
        self.url_file.close()

    def process_item(self, item, spider):

        if isinstance(item, Che360Item):
            line = '{}\n'.format(ujson.dumps(dict(item)))
            self.file.write(line)
            return item


        elif isinstance(item, Che360URLItem):
            line = '{}\n'.format(ujson.dumps(dict(item)))
            self.url_file.write(line)
            return item
