from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured(browser),
        "hemispheres": mars_hemisphere(browser),
        "weather": mars_twitter(browser),
        "facts": facts(),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data

def mars_news(browser):
    news_url = "https://mars.nasa.gov/news/"     
    browser.visit(news_url)

    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    slide = news_soup.select_one("ul.item_list li.slide")
    title = slide.find("div", class_="content_title").get_text()
    snippet = slide.find("div", class_="article_teaser_body").get_text()

    return title, snippet

def featured(browser):
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    fullsize = browser.find_by_id("full_image")
    fullsize.click()

    browser.is_element_present_by_text("more info")
    info = browser.find_link_by_partial_text("more info")
    info.click()

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    featured_img = soup.select_one("figure.lede a img")

    img_relative = featued_img.get("src")

    img_url = "https://www.jpl.nasa.gov" + img_relative

    return img_url

def mars_twitter(browser):
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    attrs = {"class": "tweet", "data-name": "Mars Weather"}
    tweet = soup.find("div", attrs=attrs)

    mars_weather = tweet.find("p", "tweet-text").get_text()

    return mars_weather

def mars_hemisphere(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(url)
    image_urls = []
    for i in range(4):

        browser.find_by_css("a.product-item h3")[i].click()

        data = scrape_hemisphere(browser.html)

        image_urls.append(data)

        browser.back()

    return image_urls

def hemisphere_scrape(html_text):
    soup = BeautifulSoup(html_text, "html.parser")

    title = soup.find("h2", class_="title").get_text()
    sample = soup.find("a", text="Sample").get("href")

    hemisphere = {
        "title": title,
        "img_url": sample
    }

    return hemisphere



def facts():
    facts_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)

    mars_facts_df = mars_facts[0]
    mars_facts_df.columns = ["description", "value"]
    mars_facts_df.set_index(["description"], inplace=True)


    # mars_html = mars_facts_df.to_html()

    return mars_facts_df.to_html(classes="table table-striped")








