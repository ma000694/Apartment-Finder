from selectolax.parser import HTMLParser
from playwright.sync_api import sync_playwright


def getContent(url):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=0)
        try:
            page.wait_for_selector("ul.allAmenities")
            page.wait_for_selector("ul.unit-specs li")
            page.wait_for_selector("div.available-date-label")
            page.wait_for_selector("div.specs-header.no-wrap.pricing")
            page.wait_for_selector("div.specs-header")
        except Exception as e:
            print(f"ERROR: {e} on {url}");        
        html = page.content()
        browser.close()
        return html

def getAmenities(html):
    amenity_list = []

    tree = HTMLParser(html)
    rentals = tree.css("ul.allAmenities li")

    for rental in rentals:
        rentalTxt = rental.text()
        isvaild = True
        for i in range(len(rentalTxt) - 1):
            if rentalTxt[i].islower() and rentalTxt[i+1].isupper():
                isvaild = False
        if isvaild:
            amenity_list.append(rentalTxt)
    return amenity_list


def getDetails(html):
    detail_list = []

    tree = HTMLParser(html)
    rentals = tree.css("ul.unit-specs li")

    if len(rentals) == 3:
        for rental in rentals:
            detail_list.append(rental.text())
    if len(rentals) == 2:
        for rental in rentals:
            detail_list.append(rental.text())
        detail_list.append("SQFT not found")

    try:
        detail_list.append(tree.css_first("div.available-date-label").text().replace(","," "))
    except:
        detail_list.append("Availability date not found")
    return detail_list

def getRent(html):

    tree = HTMLParser(html)
    try:
        rent = tree.css_first("div.specs-header.no-wrap.pricing").text()
        rentLs = rent.split()
        rent = rentLs[0]

    except AttributeError:
        rent = "rent not found"

    return rent.replace(",","")

def getRoomType(html):

    tree = HTMLParser(html)
    try:
        roomtype = tree.css_first("div.specs-header").text()
    except:
        roomtype = "room type not found"

    return roomtype

def getPropertyUrl(html):
    tree = HTMLParser(html)
    try:
        url = tree.css_first(".baseAlignedIcon.propertyWebsiteLink.propertyInfo.js-externalUrl").attributes["href"]
    except:
        url = "url not found"

    return url

print(getPropertyUrl(getContent("https://www.apartments.com/holden-house-saint-paul-mn/dmxeevk/")))