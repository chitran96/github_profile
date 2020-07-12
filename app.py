import crochet
crochet.setup()

import time, os
from flask import Flask, flash, redirect, render_template, \
     request, url_for, jsonify
import flask_excel as excel

from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher

from github_profile.spiders.link import LinkSpider
from github_profile.spiders.info import InfoSpider


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

crawl_runner = CrawlerRunner()
output_data = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl', methods=['GET', 'POST'])
def crawl():
    error = None
    if os.path.exists("links.json"): 
        os.remove("links.json")

    if os.path.exists("result.json"): 
        os.remove("result.json")
        
    if request.method == 'POST':
        # if request.form['username'] != 'admin' or \
        #         request.form['password'] != 'secret':
        #     error = 'Invalid credentials'
        # else:
        #     flash('You were successfully logged in')
        #     return redirect(url_for('index'))
        search_list = []
        search_list.append("http://github.com")
        for idx in range(1, int(request.form['pages'])+1):
            search_list.append("https://github.com/search?p=" + str(idx) + "&q=language%3A" + request.form['lang'] + "+location%3A" + request.form['loc'] + "&type=Users")
        
        print(search_list)
        
        scrape_links_with_crochet(search_list=search_list) # Passing that URL to our Scraping Function

        time.sleep(5) # Pause the function while the scrapy spider is running

        scrape_profile_with_crochet()

        time.sleep(5)
    
        return jsonify(output_data) # Returns the scraped data after being 

    return render_template('crawl.html', error=error)


@crochet.run_in_reactor
def scrape_links_with_crochet(search_list):
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
    dispatcher.connect(_mock_crawler_result, signal=signals.item_scraped)
    
    # This will connect to the LinkSpider function in our scrapy file and after each yield will pass to the crawler_result function.
    eventual = crawl_runner.crawl(LinkSpider, category=search_list)
    
    return eventual

#This will append the data to the output data list.
def _crawler_result(item, response, spider):
    output_data.append(dict(item))

def _mock_crawler_result(item, response, spider):
    # mock only, maybe add DEBUG here
    pass

def scrape_profile_with_crochet():

    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

    eventual = crawl_runner.crawl(InfoSpider)
    return eventual


if __name__ == '__main__':
    app.run()
