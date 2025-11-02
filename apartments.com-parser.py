import httpx
from selectolax.parser import HTMLParser
from playwright.sync_api import sync_playwright


def getAmenities(url):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        html = page.content()
        browser.close()

    tree = HTMLParser(html)
    rentals = tree.css("ul.allAmenities li")

    amenity_list = []
    for rental in rentals:
        amenity_list.append(rental.text())
    print(amenity_list)
