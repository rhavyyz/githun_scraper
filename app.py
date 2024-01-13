from flask import Flask, request, jsonify
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process

import json

app = Flask(__name__)

def run_spider(user):

    def run():
        process = CrawlerProcess(get_project_settings())
        process.crawl('githubspider', user=user)
        process.start()

    return run

@app.route('/scrape/<user>', methods=['GET'])
def scrape(user):
    try:
        p = Process(target=run_spider(user))
        
        p.start()

        p.join()
        
        with open("output.json", 'r') as file:
            return json.load(file)
    
    except Exception as e :

        print(e)

        return "bosta", 400

if __name__ == '__main__':
    app.run()