# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from github_scraper.items import UserItem, ReadmeUserItem,RepositoryItem, ReadmeRepositoryItem
from scrapy.exceptions import DropItem

from functools import cmp_to_key

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

        return item


    def close_spider(self, spider):

        self.__json["repositories"] = sorted(self.__repo.values(), key=cmp_to_key(lambda i1, i2 : i1["priority"] < i2["priority"]))

        for pos, repo in enumerate(self.__json["repositories"]):
            if "categories" in repo:
                for category in repo["categories"]:
                    if category in self.__json["categories"]:
                        self.__json["categories"][category].append(pos)
                    else:
                        self.__json["categories"][category] = [pos]

                del repo["categories"]
            
            if "priority" in repo: 
                del repo["priority"]

        print(f"\n\n\n\t JSON \n{self.__json}\n\t SIZE\n{len(self.__json['repositories'])}")


class StripStringsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)        
        names = adapter.field_names()
        
        for name in names:
            if isinstance( adapter.get(name), str):
                adapter[name] = adapter.get(name).strip()
        return item

