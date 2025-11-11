import httpx
from selectolax.parser import HTMLParser
from playwright.sync_api import sync_playwright
from getUrls import getUrls


def get_content(url):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        html = page.content()
        browser.close()
        return html

def getAmenities(url):
    amenity_list = []
    html = get_content(url)

    tree = HTMLParser(html)
    rentals = tree.css("ul.allAmenities li")

    for rental in rentals:
        amenity_list.append(rental.text())
    return amenity_list

def getDetails(url):
    detail_list = []
    html = get_content(url)

    tree = HTMLParser(html)
    rentals = tree.css("ul.unit-specs li")

    for rental in rentals:
        detail_list.append(rental.text())
    return detail_list