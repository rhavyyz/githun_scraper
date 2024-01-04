from typing import Iterable
import scrapy
from scrapy.http import Request

from github_scraper.items import UserItem, ReadmeItem

class GithubspiderSpider(scrapy.Spider):
    __BASE_URL  = "https://github.com/"
    user = "rhavyyz"


    name = "githubspider"
    allowed_domains = ["github.com"]
    # start_urls = ["https://github.com"]

    def start_requests(self) -> Iterable[Request]:
        return [Request(self.__BASE_URL + self.user, self.parse_profile)]

    def parse_profile(self, response):
        user = UserItem()
        
        user["name"] = response.css("h1.vcard-names span.p-name.vcard-fullname.d-block.overflow-hidden ::text").get()
        user["nickname"] = response.css("h1.vcard-names span.p-nickname.vcard-username.d-block ::text").get()
        user["bio"] = response.css("div.p-note.user-profile-bio.mb-3.js-user-profile-bio.f4 div ::text").get()
        user["picture_url"] = response.css("div.position-relative.d-inline-block.col-2.col-md-12.mr-3.mr-md-0.flex-shrink-0 a img ::attr(src)").get()

        yield user
        yield response.follow(response.request.url + "?tab=repositories", self.parse_repo_page)

    def parse_repo_page(self, response):
        repos = response.css("#user-repositories-list ul li")

        for repo in repos:
            description = repo.css("p ::text").get()

            url = repo.css("h3 a ::attr(href)").get()

    'user-repositories-list'