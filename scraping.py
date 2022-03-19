#!/usr/bin/env python
# coding: utf-8

# In[22]:


# import Splinter andBeautifulSoup

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# import pandas
import pandas as pd


# In[23]:


# set up executable path
executable_path={"executable_path": ChromeDriverManager().install()}
browser=Browser("chrome", **executable_path, headless=False)


# In[24]:


#assign url and visit browser
url="https://redplanetscience.com/"
browser.visit(url)

#optional delay for loading the page
browser.is_element_present_by_css("div.list_text", wait_time=1)


# In[25]:


# set up HTML parser
html=browser.html
news_soup=soup(html, "html.parser")
slide_elem=news_soup.select_one("div.list_text")


# In[26]:


slide_elem.find("div", class_="content_title")


# In[27]:


#use the parent element to find the first "a" tag and save it as `news_title`
news_title=slide_elem.find("div", class_="content_title").get_text()
news_title


# In[28]:


news_p=slide_elem.find("div", class_="article_teaser_body").get_text()
news_p


# ### Featured Images

# In[29]:


# set up the URL
url="https://spaceimages-mars.com/"

#visit URL
browser.visit(url)


# In[30]:


#Find and click the full image button
full_image_elem=browser.find_by_tag("button")[1]
full_image_elem.click()


# In[31]:


#Parse the resulting html with soup
html=browser.html
img_soup=soup(html, "html.parser")


# In[32]:


# find the relative image url
image_url_rel=img_soup.find("img", class_="fancybox-image").get("src")
img_url_rel


# In[33]:


# use the base URL to create an absolute URL
img_url=f"https://spaceimages-mars.com/{img_url_rel}"
img_url


# In[34]:


# copy a table's info from one page and place into application


# In[37]:


# scrape the entire table using pandas' .read_html() function

# convert the html table into a pandas dataframe
# read_html() searches and returns all tables found in the HTML. index 0 means only return first table found
df=pd.read_html("https://galaxyfacts-mars.com/")[0]
df.columns=["description", "Mars", "Earth"]
df.set_index("description", inplace=True)
df


# In[38]:


# convert pandas dataframe back into html
df.to_html()


# In[40]:


# end the automated browsing session.
browser.quit()


# In[ ]:


# to fully automate the scrapting, need to convert to .py file

