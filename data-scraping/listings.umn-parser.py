import httpx
from selectolax.parser import HTMLParser

# from testing button clicks
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# import time

# for listings.umn.edu

url = "https://listings.umn.edu/listing?rent_style=per_person"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"}
resp = httpx.get(url, headers=headers, verify=False)
html = HTMLParser(resp.text)

# from testing button clicks
# webdriver_service = Service('/path/to/chromedriver') 
# driver = webdriver.Chrome(service=webdriver_service)
# driver.get(url)

# from testing button clicks
# takes a url (listings.umn.edu) and constantly finds load more button at bottom of webpage and simulates a click
# def loadMore(url):
#     button = driver.find_element(By.CLASS_NAME, "btn my-3 btn-success btn-block")
#     button.click()
#     time.sleep(2)

# takes listings.umn.edu url and return list of listings element nodes
def getListings(url):
    return(html.css("div.campusList div.c-list"))

# takes given list of listings and returns a list of corresponding prices (what is show on front page)
def getPrices(listings):
    prices = []
    for listing in listings:
        rent_style_element = listing.css_first("em.rent_style")
        if rent_style_element:
            prices.append(str.strip(rent_style_element.text()))
    return prices

# takes given list of listings and returns a list of corresponding IDs
def getIDs(listings):
    ids = []
    for listing in listings:
        attributes = listing.attributes
        ids.append(attributes["data-property-id"])
    return ids

#takes given list of listing IDs and returns a list of links
def getLinks(ids):
    links = []
    for id in ids:
        links.append("https://listings.umn.edu/listing?property=" + id)
    return links


        
# testing
# loadMore(url)
# listings = getListings(url)
# prices = getPrices(listings)
# print(prices)
# ids = getIDs(listings)
# print(ids)
# links = getLinks(ids)
# print(links)