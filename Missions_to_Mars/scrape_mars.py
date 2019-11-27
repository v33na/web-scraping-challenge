# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 
import pymongo

# Initialize browser
def init_browser(): 
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    #Mac Users
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #return Browser('chrome', **executable_path, headless=False)

# Create Mission to Mars global dictionary that can be imported into Mongo
#mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():
    

    # Initialize browser 
    browser = init_browser()

    #browser.is_element_present_by_css("div.content_title", wait_time=1)

    # Visit Nasa news url through splinter module
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the latest element that contains news title and news_paragraph
    news_data = {}
    titles = [] 
    news_title = soup.find('div', class_='content_title')
    for i in news_title:
        titles.append(i.text)
    
    paragraphs = []
    news_paragraph= soup.find_all('div',class_="article_teaser_body")
    for i in news_paragraph:
        paragraphs.append(i.text)
    
        # Dictionary entry from MARS NEWS
    news_data["news_title"] = titles[0]
    news_data["paragraph_text_1"] = paragraphs[0]
    news_data["paragraph_text_2"] = paragraphs[1]

    return news_data

    #finally:

    #browser.quit()

# FEATURED IMAGE
def scrape_mars_image():

 # Initialize browser 
    browser = init_browser()
    browser.is_element_present_by_css("img.jpg", wait_time=1)

    # Visit Mars Space Images through splinter module
    #image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    #browser.visit(image_url_featured)# Visit Mars Space Images through splinter module

    
    browser = init_browser()
    # HTML Object 
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    images= soup.find_all("div",class_ = 'img')
    featured_images = []
    for image in images:
        featured_images.append(image.img['src'])
    featured_image_url = 'https://www.jpl.nasa.gov/'+ featured_images[0]
    # Display full link to featured image
    print(featured_image_url)
    # Dictionary entry from FEATURED IMAGE
    #mars_info['featured_image_url'] = featured_image_url 
    #close_browser(browser)    
    return featured_image_url
  #finally:

    #browser.quit()

# Mars Weather 
def scrape_mars_weather():


        # Initialize browser 
        browser = init_browser()

        #browser.is_element_present_by_css("div", wait_time=1)

        # Visit Mars Weather Twitter through splinter module
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # HTML Object 
        html_weather = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_weather, 'html.parser')

        # Find all elements that contain tweets
        mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        print(mars_weather)
        
        # Dictionary entry from WEATHER TWEET
        #mars_info['weather_tweet'] = weather_tweet
        #close_browser(browser)
        return mars_weather
     #finally:

       # browser.quit()


# Mars Facts
def scrape_mars_facts():

    # Visit Mars facts url 
    url_facts = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    table = pd.read_html(url_facts)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    df_mars_facts = table[0]

    # Assign the columns `['Parameter', 'Values']`
    df_mars_facts.columns = ['Parameter','Values']

    # Set the index to the `Parameter` column 
    df_mars_facts.set_index(['Parameter'])

    # Save html code to folder Assets
    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_html_table

    # Dictionary entry from MARS FACTS
    #mars_info['mars_facts'] = mars_html_table

    return mars_html_table


# MARS HEMISPHERES


def scrape_mars_hemispheres():

    

    # Initialize browser 
    browser = init_browser()
    # Visit hemispheres website through splinter module 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov' 

    # Loop through the items previously stored
    for i in items: 
            # Store title
        title = i.find('h3').text
            
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
            
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
          
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
            
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

        #mars_info['hemisphere_image_url'] = hemisphere_image_urls
        # Return mars_data dictionary 
        #close_browser(browser)
        return hemisphere_image_urls

def scrape():
    """ Function: Main scrape functionality
        Calls other functions
        Parameters: None
        Returns: combined mars_info dictionary """

    mars_info = {}

    mars_info["news_data"] = scrape_mars_news()

    mars_info["featured_image_url"] =scrape_mars_image()

    mars_info["mars_weather"] = scrape_mars_weather()

    mars_info["mars_html_table"] =scrape_mars_facts()

    mars_info["hemisphere_image_url"] =scrape_mars-hemispheres()

    # return mars_data dict
    return mars_info
#if __name__ == "__main__":
 #   print(scrape())