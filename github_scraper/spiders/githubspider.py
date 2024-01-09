from typing import Iterable
import scrapy
from scrapy.http import Request

from github_scraper.items import UserItem, ReadmeUserItem, RepositoryItem, ReadmeRepositoryItem
from utils.parse_repo_desciption import parse_repo_description


class GithubspiderSpider(scrapy.Spider):
    __BASE_URL  = "https://github.com/"
    user = "rhavyyz"
    __ADD_IF_NOT_FOUND = True

    # Assuming there always will be a main branch which is false
    # so a later update would be scrape a branch that exists
    def readme_url(self, repo_name):
        return f"https://raw.githubusercontent.com/{self.user.strip()}/{repo_name.strip()}/main/README.md"

    name = "githubspider"
    allowed_domains = ["github.com", "raw.githubusercontent.com"]


    def start_requests(self) -> Iterable[Request]:
        return [Request(self.__BASE_URL + self.user, self.parse_profile)]

    # ----------------------------

    def parse_user_readme(self, response):
        content = response.css("body").get()[6:-7]
            
        if content is None:
            content = ''

        readme = ReadmeUserItem()
        readme["readme"] = content

        yield readme

    def parse_repo_readme(self, response):
        content = response.css("body").get()[6:-7]
            
        if content is None:
            content = ''

        readme = ReadmeRepositoryItem()
        readme["readme"] = content
        readme["name"] = response.request.url.split("/")[5]

        yield readme


    # ----------------------------

    def parse_profile(self, response):
        user = UserItem()
        
        user["name"] = response.css("h1.vcard-names span.p-name.vcard-fullname.d-block.overflow-hidden ::text").get()
        user["nickname"] = response.css("h1.vcard-names span.p-nickname.vcard-username.d-block ::text").get()
        user["bio"] = response.css("div.p-note.user-profile-bio.mb-3.js-user-profile-bio.f4 div ::text").get()
        user["picture_url"] = response.css("div.position-relative.d-inline-block.col-2.col-md-12.mr-3.mr-md-0.flex-shrink-0 a img ::attr(src)").get()

        yield user
        yield response.follow(response.request.url + "?tab=repositories", self.parse_repo_page)
        yield response.follow(self.readme_url(self.user) ,self.parse_user_readme)


    def parse_repo_page(self, response):
        repos = response.css("#user-repositories-list ul li")
        for repo in repos:
            description, include, categories, priority  = parse_repo_description(repo.css("p ::text").get(), self.__ADD_IF_NOT_FOUND)
            if not include:
                continue
            
            name = repo.css("h3 a ::text").get()
            relative_path = repo.css("h3 a ::attr(href)").get()

            repository = RepositoryItem()

            yield response.follow(self.readme_url(name), self.parse_repo_readme)

            repository["url"] = self.__BASE_URL + self.user + relative_path
            repository["name"] = name
            repository["description"] = description
            repository["priority"] = priority
            repository["categories"] = categories

            yield repository
