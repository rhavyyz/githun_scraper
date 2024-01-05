# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class UserItem(scrapy.Item):
    nickname = scrapy.Field()
    name = scrapy.Field()
    bio = scrapy.Field()
    about = scrapy.Field()
    picture_url = scrapy.Field()
    
class ReadmeUserItem(scrapy.Item):
    about = scrapy.Field()

class RepositoryItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    readme = scrapy.Field()
    priority = scrapy.Field()
    categories = scrapy.Field()