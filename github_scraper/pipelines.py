# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from github_scraper.items import UserItem, ReadmeUserItem,RepositoryItem
from scrapy.exceptions import DropItem

class GithubScraperPipeline:
    def open_spider(self, spider):
        self.__json = {
            "user": dict(),
            "repositories": [],
            "categories": dict()
        }


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)        
        names = adapter.field_names()

        if isinstance(item, ReadmeUserItem) and (adapter.get(list(names)[0]) is None or adapter.get(list(names)[0]) == ''):
            raise DropItem()

        if isinstance(item, UserItem) or isinstance(item, ReadmeUserItem):
            for name in names:
                self.__json["user"][name] = adapter.get(name)

        if isinstance(item, RepositoryItem):
            aux = dict()
            for name in names:
                aux[name] = adapter.get(name)
            self.__json["repositories"].append(aux)

        return item


    def close_spider(self, spider):
        print("")

class StripStringsPipiline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)        
        names = adapter.field_names()
        
        for name in names:
            if isinstance( adapter.get(name), str):
                adapter[name] = adapter.get(name).strip()
                # print(adapter.get(name))
        return item

