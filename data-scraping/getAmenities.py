from selectolax.parser import HTMLParser

async def safeGoto(browser, url):
    for _ in range(25):
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded")
            html = await page.content()

            if "access denied" in html.lower() or "<html></html>" in html.lower():
                await page.close()
                continue

            return page, html
        
        except:
            await page.close()
            continue

    raise Exception(f"safeGoto failed after 25 attempts: {url}")
    

async def getContent(url, browser):
    rentalKey = url.split("#")[1].split("-")[0]
    selector = f'button[data-rentalkey="{rentalKey}"].js-viewModelDetails-modal'
    baseUrl = url.split("#")[0]

    while True:
        page, html = await safeGoto(browser, baseUrl)
    
        try:
            await page.wait_for_selector("button.actionLinks.js-viewModelDetails-modal",timeout=10000)
            await page.locator(selector).first.click()
            break
        except:
            pass

        try:
            await page.wait_for_selector("button.js-showUnavailableFloorPlansButton",timeout=10000)
            await page.locator('button[aria-expanded="false"].js-showUnavailableFloorPlansButton').first.click()
            await page.locator(selector).first.click()
            break
        except:
            pass

    while True:
        try:
            await page.wait_for_selector("ul.unit-specs li",timeout=10000)
            await page.wait_for_selector("div.specs-header",timeout=10000)
            html = await page.content()
            await page.close()
            return html
        except Exception as e:
            print(f"ERROR: {e} on {url}")
            await page.close()
            return await getContent(url, browser)

async def getPageContent(url, browser):
    while True:
        page, html = await safeGoto(browser, url)
        try:                
            await page.wait_for_selector("h1#propertyName.propertyName",timeout=10000)
            await page.wait_for_selector("div.propertyAddressContainer",timeout=10000)
            html = await page.content()
            await page.close()
            return html
        
        except Exception as e:
            print(f"ERROR loading page {url}:\n{e}")
            await page.close()
            continue

def getNameAndAddress(html):
    tree = HTMLParser(html)
    try:
        name = tree.css_first("h1#propertyName.propertyName").text().replace("\n","").replace("  ","")
    except:
        name = "Name not found"
    try:
        address = tree.css_first("div.propertyAddressContainer").text().strip().replace(","," ").replace("\n", "").replace("  ","").replace("Property Website","").replace("MN","MN ")
    except:
        address = "Address not found"
    return [name,address]

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

    return roomtype.replace(","," ")

def getPropertyUrl(html):
    tree = HTMLParser(html)
    try:
        url = tree.css_first(".baseAlignedIcon.propertyWebsiteLink.propertyInfo.js-externalUrl").attributes["href"]
    except:
        url = "url not found"

    return url
