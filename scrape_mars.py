
#%%
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd


#%%
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


#%%
def scrape():
    mars_data = {}
    
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    article_headlines = []

    for title in soup.find_all('div',class_="content_title"):
        headline = title.find('a').text
        mars_data['title'] = headline
        article_headlines.append(headline)

    article_snippets = []

    for snippet in soup.find_all('div', class_='article_teaser_body'):
        details = snippet.text
        mars_data['snippet'] = details
        article_snippets.append(details)

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html = browser.html

    soup = BeautifulSoup(html,'html.parser')

    featured_image = soup.find('div', class_='img')
    featured_image.get('src')

    featured = soup.find('div', class_='carousel_items')
    featured_image = featured.find('article')['style']
    featured_image_url = featured_image.replace("background-image: url('/", '')
    featured_image_url = featured_image_url.replace("');", '')

    featured_image_url = 'https://www.jpl.nasa.gov/' + featured_image_url

    mars_data['featured_img'] = featured_image_url

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html = browser.html

    soup = BeautifulSoup(html,'html.parser')

    mars_weather = soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

    weather_string = 'InSight sol '
    for weather_tweet in mars_weather:
        if weather_string in weather_tweet.text:
            weather = weather_tweet.text
            mars_data['weather_tweets'] = weather

    facts_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)

    soup = BeautifulSoup(html,'html.parser')

    mars_facts_df = mars_facts[0]
    mars_facts_df.columns = ["Category", "Value"]
    mars_facts_df.set_index(["Category"], inplace=True)


    mars_html = mars_facts_df.to_html()

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    html = browser.html

    soup = BeautifulSoup(html,'html.parser')

    hemisphere_titles = []
    hemisphere_img_urls = []
    link_urls = []
    hemisphere_dictionaries = []

    base_url = 'https://astrogeology.usgs.gov/'

    url_scrape = soup.find_all('div', class_='description')

    for link in url_scrape:
        url = link.find('a', class_='itemLink')
        individual_url = url.get('href')
        individual_url = base_url + individual_url
        link_urls.append(individual_url)
    

    title_scrape = soup.find_all('div', class_='description')

    for title in title_scrape:
        title_text = title.find('h3').text
        hemisphere_titles.append(title_text)
    
    mars_data['hemisphere_titles'] = hemisphere_titles

    cerberus_url = 'https://astrogeology.usgs.gov//search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(cerberus_url)
    cerb_html = browser.html
    cerb_soup = BeautifulSoup(cerb_html, 'html.parser')
        
    cerb_img = cerb_soup.find("img", class_="wide-image")["src"]
    cerb_img_url = base_url + cerb_img
    hemisphere_img_urls.append(cerb_img_url)

    shia_url = 'https://astrogeology.usgs.gov//search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(shia_url)
    shia_html = browser.html
    shia_soup = BeautifulSoup(shia_html, 'html.parser')
        
    shia_img = shia_soup.find("img", class_="wide-image")["src"]
    shia_img_url = base_url + shia_img
    hemisphere_img_urls.append(shia_img_url)

    syrtis_url = 'https://astrogeology.usgs.gov//search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(syrtis_url)
    syrtis_html = browser.html
    syrtis_soup = BeautifulSoup(syrtis_html, 'html.parser')
        
    syrtis_img = syrtis_soup.find("img", class_="wide-image")["src"]
    syrtis_img_url = base_url + syrtis_img
    hemisphere_img_urls.append(syrtis_img_url)

    valles_url = 'https://astrogeology.usgs.gov//search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(valles_url)
    valles_html = browser.html
    valles_soup = BeautifulSoup(valles_html, 'html.parser')
        
    valles_img = valles_soup.find("img", class_="wide-image")["src"]
    valles_img_url = base_url + valles_img
    hemisphere_img_urls.append(valles_img_url)

    mars_data['hemisphere_images'] = hemisphere_img_urls

    return mars_data