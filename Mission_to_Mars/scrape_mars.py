def scrape():
    import time
    from splinter import Browser
    import re
    from bs4 import BeautifulSoup as bs
    import pandas as pd

    # chromedriver
    def init_browser():
        # @NOTE: Replace the path with your actual path to the chromedriver
        executable_path = {"executable_path": "C://bin/chromedriver.exe"}
        return Browser("chrome", **executable_path, headless=True)

    # function for creating soup
    def soupify(sleep_time):
        # sleep_time is the number of seconds you want it to wait
        browser.visit(url)
        time.sleep(sleep_time)
        html = browser.html
        soup = bs(html, "html.parser")
        return soup

    # dictionary for all data
    mars_data = {}

    # initialize the browser
    browser = init_browser()


    # ### NASA Mars News

    # visit and scrape mars.nasa.gov
    # set url
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    # soupify the webpage
    soup = soupify(2)

    # find the title and paragraph text of the first article
    news_title = soup.find_all("div", "content_title")[1].text
    news_p = soup.find_all("div", "article_teaser_body")[0].text

    # add the data to the dictionary
    mars_data.update({"news_title": news_title, "news_p": news_p})


    # ### JPL Mars Space Images - Featured Image

    # visit and scrape jpl.nasa.gov
    # set url
    base_url = "https://www.jpl.nasa.gov"
    url = base_url + "/spaceimages/?search=&category=Mars" # seperated url to make image path later
    # soupify the webpage
    soup = soupify(1)

    # find and print url of the featured image
    relative_image_path = soup.find(id='full_image')['data-fancybox-href']
    featured_image_url = base_url + relative_image_path

    # add data to the dictionary
    mars_data.update({"featured_image_url": featured_image_url})

    # ### Mars Weather

    # visit and scrape twitter.com
    url = "https://twitter.com/marswxreport?lang=en"
    soup = soupify(3)

    # find the text of the latest tweet
    mars_weather = soup.find(text=re.compile("InSight sol"))

    # add data to the dictionary
    mars_data.update({"mars_weather": mars_weather})

    # ### Mars Facts

    # visit and scrape space-facts.com/mars
    url = "https://space-facts.com/mars/"

    # read in html tables
    tables = pd.read_html(url)
    # make the first table into a dataframe
    df = tables[0]

    # convert df to html
    mars_planet_profile = df.to_html(index=False)
    # create html file
    df.to_html('table.html')

    # add data to the dictionary
    mars_data.update({"mars_planet_profile": mars_planet_profile})


    # ### Mars Hemispheres

    # visit and scrape astrogeology.usgs.gov
    base_url = "https://astrogeology.usgs.gov"
    url = base_url + "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    soup = soupify(2)

    # find the images of all 4 mars hemispheres
    # make a list for the relative link paths 
    relative_links = []
    hemisphere_image_urls = []
    # find link for all four images
    relative_links.append(soup.find_all("a", "product-item")[0]["href"])
    relative_links.append(soup.find_all("a", "product-item")[2]["href"])
    relative_links.append(soup.find_all("a", "product-item")[4]["href"])
    relative_links.append(soup.find_all("a", "product-item")[6]["href"])

    for link in relative_links:
        url = base_url + link
        soup = soupify(1)
        new_link = base_url + soup.find("img", "wide-image")["src"]
        raw_title = soup.find("h2", "title").text
        title = raw_title.rsplit(' ', 1)[0]
        link_dict = {"title": title, "img_url": new_link}
        hemisphere_image_urls.append(link_dict)

    # add data to the dictionary
    mars_data.update({"mars_hemispheres": hemisphere_image_urls})

    # quit the browser
    browser.quit()

    return mars_data