from selectolax.parser import HTMLParser # parses HTML to return a queryable tree of HTML

# creates browser to access webpage, skipping blank or unavailable/denied... returns live page and it's html
async def safeGoto(browser, url):

    # tries to load 25 times
    for _ in range(25):

        # create new tab to access webpage
        page = await browser.new_page()

        # tries to open page with url, waiting for HTML
        try:
            await page.goto(url, wait_until="domcontentloaded")
            html = await page.content()

            # unable to access, err...
            if "access denied" in html.lower() or "<html></html>" in html.lower():
                await page.close()
                continue

            # return webpage and html
            return page, html
        
        # close webpage and try again, for 25 times...
        except:
            await page.close()
            continue

    # failed all 25 times...
    raise Exception(f"safeGoto failed after 25 attempts: {url}")
    

# goes to property page, clicks on listing, and return HTML of page
async def getContent(url, browser):
    
    # splits url by # and -, using only 1 and 0 instance (0-base).
    rentalKey = url.split("#")[1].split("-")[0]

    # used to find exact button to press using rentalKey above.
    selector = f'button[data-rentalkey="{rentalKey}"].js-viewModelDetails-modal'

    # returns site url: https://www.apartments.com/...
    baseUrl = url.split("#")[0]

    # infinite loop
    while True:

        # extract page and html from function that opens browser
        page, html = await safeGoto(browser, baseUrl)
    
        # looking for specific button to get info about specific room type.
        try:
            await page.wait_for_selector("button.actionLinks.js-viewModelDetails-modal",timeout=10000)
            await page.locator(selector).first.click()
            break
        except:
            pass

        # looking for specific button, "unavailable button".
        try:
            await page.wait_for_selector("button.js-showUnavailableFloorPlansButton",timeout=10000)
            await page.locator('button[aria-expanded="false"].js-showUnavailableFloorPlansButton').first.click()
            await page.locator(selector).first.click()
            break
        except:
            pass

    # another infinite loop
    while True:

        # looking for two elements, rent and room type, grabs and return html and closes browser.
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

# loads property main overview page, and returns html.
async def getPageContent(url, browser):

    # infinite loop
    while True:

        # extract html and page
        page, html = await safeGoto(browser, url)

        # looking for two elements, property name, and address, return html, and close.
        try:                # 
            await page.wait_for_selector("h1#propertyName.propertyName",timeout=10000)
            await page.wait_for_selector("div.propertyAddressContainer",timeout=10000)
            html = await page.content()
            await page.close()
            return html
        
        except Exception as e:
            print(f"ERROR loading page {url}:\n{e}")
            await page.close()
            continue

# takes property overview page (html), and returns name and address of property.
def getNameAndAddress(html):

    # creates HTML tree, queryable.
    tree = HTMLParser(html)

    # looking for property name
    try:
        name = tree.css_first("h1#propertyName.propertyName").text().replace("\n","").replace("  ","")
    except:
        name = "Name not found"

    # looking for property address
    try:
        address = tree.css_first("div.propertyAddressContainer").text().strip().replace(","," ").replace("\n", "").replace("  ","").replace("Property Website","").replace("MN","MN ")
    except:
        address = "Address not found"

    # return name and address
    return [name,address]

# extract amenities from listings, using html, filtering out bad text.
def getAmenities(html):

    # list of amenities
    amenity_list = []

    # creates HTML tree, queryable.
    tree = HTMLParser(html)

    # looking for amenities, returns as list
    rentals = tree.css("ul.allAmenities li")

    # iterate through amenities list
    for rental in rentals:

        # textify
        rentalTxt = rental.text()

        isvaild = True

        # error handling, looking for concatenated words to skip.
        for i in range(len(rentalTxt) - 1):
            if rentalTxt[i].islower() and rentalTxt[i+1].isupper():
                isvaild = False

        # add amenity into list
        if isvaild:
            amenity_list.append(rentalTxt)

    # return list of amenities
    return amenity_list

# extracts extra info regarding listing, ie: beds, baths, sqft, and availability.
def getDetails(html):

    # list of details of listing
    detail_list = []

    # creates HTML tree, queryable.
    tree = HTMLParser(html)

    # looking for unit information, returns as list
    rentals = tree.css("ul.unit-specs li")

    # if bed, bath, and sqft exist
    if len(rentals) == 3:
        for rental in rentals:
            detail_list.append(rental.text())

    # if only bed and bath exist, no sqft.
    if len(rentals) == 2:
        for rental in rentals:
            detail_list.append(rental.text())
        detail_list.append("SQFT not found")

    # looking for availability
    try:
        detail_list.append(tree.css_first("div.available-date-label").text().replace(","," "))
    except:
        detail_list.append("Availability date not found")

    # return listing detail list
    return detail_list

# extract rent for listing, removes commas from figures. ex: 1,000 -> 1000
def getRent(html):

    # creates HTML tree, queryable.
    tree = HTMLParser(html)

    # looking for rent info from tree
    try:
        rent = tree.css_first("div.specs-header.no-wrap.pricing").text()
        rentLs = rent.split()
        rent = rentLs[0]

    except AttributeError:
        rent = "rent not found"

    # return rent cost, without commas. ex: 1,000 -> 1000, CSV protection
    return rent.replace(",","")

# extract room type, ex: 1 Bed, Studio, etc...
def getRoomType(html):

    # creates HTML tree, queryable.
    tree = HTMLParser(html)

    # looking for room type info
    try:
        roomtype = tree.css_first("div.specs-header").text()
    except:
        roomtype = "room type not found"

    # returns room type without commas, CSV protection
    return roomtype.replace(","," ")

# extract property url
def getPropertyUrl(html):

    # creates HTML tree, queryable.
    tree = HTMLParser(html)

    # looking for url of property
    try:
        url = tree.css_first(".baseAlignedIcon.propertyWebsiteLink.propertyInfo.js-externalUrl").attributes["href"]
    except:
        url = "url not found"

    # return url
    return url
