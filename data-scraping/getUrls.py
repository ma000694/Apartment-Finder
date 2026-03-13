from selectolax.parser import HTMLParser # reads webpage
from getAmenities import safeGoto # in-house function from getAmenities.py, opens page in browser.

# searches through apartment.com, and extract property urls.
async def getWebsiteUrls(BasewebsiteUrl, browser):
        
    # gets urls for apartment building pages
    urls = []

    # extract page and html.
    page, html = await safeGoto(browser, BasewebsiteUrl)

    # autoruns, create infinite loop, retrying until break.
    while True:
        # load webpage, searching for "a.property-link", else try again.
        try:
            await page.wait_for_selector("a.property-link",timeout=10000)
            break
        except:
            html = await page.content()
            continue

    # parses HTML to create queryable tree
    tree = HTMLParser(html)

    # searches for every "a.property-link" tag, clickable links to listings, stores as list
    apartments = tree.css("a.property-link")

    # iterate through all property from above
    for apartment in apartments:

        # extract url from href tag in HTML
        url = apartment.attributes.get("href")

        # if url not empty/null, and url not in url list, append...
        if url and url not in urls:
            urls.append(url)
    
    # close page and return list of property urls
    await page.close()
    return urls

# searches through property url, and extract apartment listings.
async def getUrls(url, browser):

    # infinite loop, keeps trying...
    while True:

        # extracts page and html, by loading page.
        page, html = await safeGoto(browser, url)

        # search for pricing grid, valid listing is legit, else close and return empty list
        try:
            await page.wait_for_selector("div.pricingGridTitleBlock",timeout=10000)
        except:
            print(f"{url} may not be an apartment.")
            await page.close()
            return []
        
        # search for unit details, else pass
        try:
            await page.wait_for_selector("button.actionLinks.js-viewModelDetails-modal",timeout=10000)
        except:
            pass

        # search for unavailable listings? clicks to find new listings?
        try:
            await page.wait_for_selector("button.js-showUnavailableFloorPlansButton",timeout=10000)
            await page.locator("button.js-showUnavailableFloorPlansButton").first.click()
            await page.wait_for_selector("button.actionLinks.js-viewModelDetails-modal",timeout=10000)
        except:
            pass

        # parses HTML to create queryable tree
        tree = HTMLParser(await page.content())

        # create list of roomTypes, and urlsToAdd, and temp...
        roomTypesCounted = []
        urlsToAdd = []
        tempUrls = []

        # search for room info, store as list
        roomInfo = tree.css("button.actionLinks.js-viewModelDetails-modal")

        # iterate through roomInfo, 1BR, 2, studio, etc...
        for room in roomInfo:
            roomType = room.attributes.get("data-rentalkey")

            if roomType not in roomTypesCounted:
                tempUrls.append(room.attributes.get("data-rentalkey") + "-1-floorPlan")
                roomTypesCounted.append(roomType)
        
        # append tempUrls to urlsToAdd
        for tempUrl in tempUrls:
            urlsToAdd.append(url + "#" + tempUrl)

        # close and return urlsToAdd
        await page.close()
        return urlsToAdd

# create and return final list of urls, property and their listings
async def getFinalUrls(urls, browser):
    finalUrls = {}
    for url in urls:
        finalUrls[url] = await getUrls(url, browser)
    return finalUrls

# return all the Urls...
async def getAllUrls(baseUrl, browser):
    urls = await getWebsiteUrls(baseUrl, browser)
    return await getFinalUrls(urls, browser)