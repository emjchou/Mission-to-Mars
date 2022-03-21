from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # set up executable path
    executable_path={"executable_path": ChromeDriverManager().install()}
    browser=Browser("chrome", **executable_path, headless=True)
    
    # set news title and paragraph variables using our mars_news() function
    news_title, news_paragraph = mars_news(browser)
    
    # create the data dictionary
    #run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }
    
    # end the automated browsing session.
    browser.quit()
    
    return data


def mars_news(browser):
    #assign url and visit browser
    url="https://redplanetscience.com/"
    browser.visit(url)

    #optional delay for loading the page
    browser.is_element_present_by_css("div.list_text", wait_time=1)

    # set up HTML parser
    html=browser.html
    news_soup=soup(html, "html.parser")
    slide_elem=news_soup.select_one("div.list_text")
    
    #add try/except for error handling
    try:
        slide_elem.find("div", class_="content_title")

        #use the parent element to find the first "a" tag and save it as `news_title`
        news_title=slide_elem.find("div", class_="content_title").get_text()

        news_p=slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p


# ### Featured Images
def featured_image(browser):
    # set up the URL
    url="https://spaceimages-mars.com/"

    #visit URL
    browser.visit(url)

    #Find and click the full image button
    full_image_elem=browser.find_by_tag("button")[1]
    full_image_elem.click()

    #Parse the resulting html with soup
    html=browser.html
    img_soup=soup(html, "html.parser")
    
    try:
        # find the relative image url
        img_url_rel=img_soup.find("img", class_="fancybox-image").get("src")

    except AttributeError:
        return None
    
    # use the base URL to create an absolute URL
    img_url=f"https://spaceimages-mars.com/{img_url_rel}"
    
    return img_url

def mars_facts():
    # copy a table's info from one page and place into application
    
    try:
        # scrape the entire table using pandas' .read_html() function

        # convert the html table into a pandas dataframe
        # read_html() searches and returns all tables found in the HTML. index 0 means only return first table found
        df=pd.read_html("https://galaxyfacts-mars.com/")[0]
    except BaseException:
        return None
    
    df.columns=["description", "Mars", "Earth"]
    df.set_index("description", inplace=True)

    # convert pandas dataframe back into html
    return df.to_html()

# Scrape hemisphere data
def hemispheres(browser):
    #visit the url
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    # create a list to hold the images and titles.
    hemisphere_image_urls = []
    hemispheres={}

    # parse the html
    html=browser.html
    mars_page=soup(html, "html.parser")

    # for each <div class="description" /> found:   
    for desc in mars_page.find_all("div", class_="description"):

        #GET IMAGE URL

        #on the main page, find the link to go to the description page, which hold the link for jpg.

        # extract the relative description url extension, then attach to base url
        desc_url_rel=desc.find("a").get("href")
        desc_url=f"{url}{desc_url_rel}"

        #visit the description url
        browser.visit(desc_url)

        #parse the new page
        html=browser.html
        desc_page=soup(html, "html.parser")

        # on the description page, find the link to the jpg image

        # extract relative image url extension, then attach to base url
        image_url_rel=desc_page.find("li").find("a").get("href")
        image_url=f"{url}{image_url_rel}"

        # GET THE TITLE
        #extract the title
        title=desc_page.find("h2", class_="title").text

        # go back to the main page (mars_page)
        browser.back()

        #save the image url into the hemispheres dict
        hemispheres["img_url"]=image_url
        hemispheres["title"]=title

        #put the dict into the hemisphere_image_urls list
        hemisphere_image_urls.append(hemispheres.copy())
        
    #close/quit the browser
    #browser.quit()

    #return the hemisphere_image_urls
    return hemisphere_image_urls
    
    
    
if __name__ == "__main__":
    #if running as script, print scraped data
    print(scrape_all())
    
