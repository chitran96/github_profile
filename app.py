import crochet
crochet.setup()

import time, os
from flask import Flask, flash, redirect, render_template, \
     request, url_for, jsonify, send_from_directory
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

    if request.method == 'POST':
        # if request.form['username'] != 'admin' or \
        #         request.form['password'] != 'secret':
        #     error = 'Invalid credentials'
        # else:
        #     flash('You were successfully logged in')
        #     return redirect(url_for('index'))
        output_data = []
        search_list = []
        search_list.append("https://github.com")
        for idx in range(1, int(request.form['pages'])+1):
            search_list.append("https://github.com/search?p=" + str(idx) + "&q=language%3A" + request.form['lang'] + "+location%3A" + request.form['loc'] + "&type=Users")
        
        print(search_list)
        
        scrape_links_with_crochet(search_list=search_list) # Passing that URL to our Scraping Function

        time.sleep(5) # Pause the function while the scrapy spider is running

        scrape_profile_with_crochet()
    
        # return jsonify(output_data) # Returns the scraped data after being 
        return redirect(url_for("crawl_result", lang=request.form['lang'], loc=request.form['loc'], time=time.time()))

    return render_template('crawl.html', error=error)

@app.route('/crawl/result-<lang>-<loc>-<time>.csv')
def crawl_result(lang, loc, time):
    return send_from_directory(".", "items.csv")

#This will append the data to the output data list.
def _crawler_result(item, response, spider):
    if spider.name == "info":
        output_data.append(dict(item))

def _spider_done(spider, reason):
    if spider.name == 'info':
        print("Done")

@crochet.wait_for(timeout=5.0)
def scrape_links_with_crochet(search_list):

    try:
        eventual = crawl_runner.crawl(LinkSpider, category=search_list)
    except Exception as err:
        # handle error here
        print(err)

    return eventual

@crochet.wait_for(timeout=60.0)
def scrape_profile_with_crochet():
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    dispatcher.connect(_spider_done, signal=signals.spider_closed)
    try:
        eventual = crawl_runner.crawl(InfoSpider)
    except Exception as err:
        # handle error here
        print(err)
    return eventual


if __name__ == '__main__':
    app.run()
