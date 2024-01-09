# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from github_scraper.items import UserItem, ReadmeUserItem,RepositoryItem, ReadmeRepositoryItem
from scrapy.exceptions import DropItem

from utils.item_dict import item_to_dict

class GithubScraperPipeline:
    def open_spider(self, spider):
        self.__json = {
            "user": dict(),
            "repositories": [],
            "categories": dict()
        }

        self.__repo = dict()


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)        
        names = adapter.field_names()

        if isinstance(item, ReadmeUserItem) and (adapter.get(list(names)[0]) is None or adapter.get(list(names)[0]) == ''):
            raise DropItem()

        if isinstance(item, UserItem) or isinstance(item, ReadmeUserItem):
            for name in names:
                self.__json["user"][name] = adapter.get(name)

        if isinstance(item, RepositoryItem) or isinstance(item, ReadmeRepositoryItem):
            d = self.__repo.get(item["name"], None)

            if d is None:
                self.__repo[item["name"]] = item_to_dict(item)
            else:
                item_to_dict(item, d)


            print("passou aquirrr", item)

        return item


    def close_spider(self, spider):

        for repo in self.__repo.values():
            self.__json["repositories"].append(repo)

        print(self.__json)

class StripStringsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)        
        names = adapter.field_names()
        
        for name in names:
            if isinstance( adapter.get(name), str):
                adapter[name] = adapter.get(name).strip()
                # print(adapter.get(name))
        return item

