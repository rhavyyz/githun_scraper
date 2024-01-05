# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from github_scraper.items import UserItem, ReadmeUserItem,RepositoryItem, ReadmeRepositoryItem
from scrapy.exceptions import DropItem
from utils.magic_value import set_value, get_value

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
        print(self.__json)

class RepositoryPipeline:

    content = ''

    def process_item(self, item, spider):
        if isinstance(item, ReadmeRepositoryItem):
            set_value(item["about"])
            print(f"about_set {get_value()}")

        elif isinstance(item, RepositoryItem):
            item["readme"] = get_value()
            print(f'about_get {item["readme"]}')
            set_value('')

        return item

class StripStringsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)        
        names = adapter.field_names()
        
        for name in names:
            if isinstance( adapter.get(name), str):
                adapter[name] = adapter.get(name).strip()
                # print(adapter.get(name))
        return item

