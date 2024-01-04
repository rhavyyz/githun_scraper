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
    name = scrapy.Field()
    nickname = scrapy.Field()
    bio = scrapy.Field()
    about = scrapy.Field()
    picture_url = scrapy.Field()
    
class ReadmeItem(scrapy.Item):
    content = scrapy.Field()