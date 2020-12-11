#Import dependencies
import pymongo
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    marsnewsURL = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(marsnewsURL)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    article= soup.select_one('ul.item_list li.slide')

    news_title = article.find('div',class_= 'content_title').get_text()
    news_title

    news_p = article.find('div',class_= 'article_teaser_body').get_text()
    news_p

    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(featured_image_url)

    clickingimg=browser.find_by_id('full_image')
    clickingimg.click()

    allinfoimg= browser.find_link_by_partial_text('more info')
    allinfoimg.click()

    html1 = browser.html
    soup1 = BeautifulSoup(html1, 'html.parser')

    images = soup1.find_all('figure',class_='lede')
    images

    allimagesURL = images[0].a["href"]
    allimagesURL

    featured_image_url = 'https://www.jpl.nasa.gov'+ allimagesURL
    featured_image_title = soup1 .find('h1', class_="media_feature_title").text.strip()
    featured_image_url
    featured_image_title

    marsurl = 'https://space-facts.com/mars/'
    table = pd.read_html(marsurl)
    table

    type(table)

    marsdf = table[0]
    marsdf.columns = ['Fact', 'Value']
    marsdf.head(9)

    html_table = marsdf.to_html()
    html_table
    html_table.replace('\n', '')

    marsdf.to_html('marstable.html')

    MarsHemispheresURL = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(MarsHemispheresURL)

    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')

    divitem = soup3.find_all('div',class_='item')
    divitem

    hemisphere_image_urls = []
    for items in divitem:
        URL = items.find('a')['href']
        title = items.find('div', class_='description').find('a').find('h3').text
        finalURL='https://astrogeology.usgs.gov'+URL
        browser.visit(finalURL)
        html=browser.html
        soup=BeautifulSoup(html,'html.parser')
        finalimage=soup.find('div',class_= 'downloads').find('ul').find('li').find('a')['href']
        hemisphere_image_urls.append({'title':title,'imageURL':finalimage})
    print(hemisphere_image_urls)

    mars_scrape_dictionary = {
        "title": news_title,
        "paragraph": news_p,
        "print_image_url": featured_image_url,
        'featured_image_title': featured_image_title,
        "mars_df": marsdf,
        "mars_hemi": hemisphere_image_urls,
    }

    return mars_scrape_dictionary


    