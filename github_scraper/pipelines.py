# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from github_scraper.items import UserItem, ReadmeItem
from scrapy.exceptions import DropItem

class GithubScraperPipeline:
    def open_spider(self, spider):
        self.__json = {
            "user": {},
            "repositories": [],
            "categories": {

            }
        }


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)        
        names = adapter.field_names()

        if item is ReadmeItem and (adapter.get(names[0]) is None or adapter.get(names[0]) == ''):
            raise DropItem()

        for name in names:
            if isinstance( adapter.get(name), str):
                adapter[name] = adapter.get(name).strip()
                print(adapter.get(name))

        if item is UserItem or item is ReadmeItem:
            for name in names:
                self.__json[name] = adapter.get(name)

        return item


    def close_spider(self, spider):
        print(self.__json)
