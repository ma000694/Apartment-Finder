from selectolax.parser import HTMLParser
from getAmenities import safeGoto

async def getWebsiteUrls(BasewebsiteUrl, browser):
        
    # gets urls for apartment building pages
    urls = []

    page, html = await safeGoto(browser, BasewebsiteUrl)
    while True:
        try:
            await page.wait_for_selector("a.property-link",timeout=10000)
            break
        except:
            html = await page.content()
            continue

    tree = HTMLParser(html)
    apartments = tree.css("a.property-link")

    for apartment in apartments:
        url = apartment.attributes.get("href")
        if url and url not in urls:
            urls.append(url)
    
    await page.close()
    return urls

async def getUrls(url, browser):
    while True:
        page, html = await safeGoto(browser, url)

        try:
            await page.wait_for_selector("div.pricingGridTitleBlock",timeout=10000)
        except:
            print(f"{url} may not be an apartment.")
            await page.close()
            return []
        
        try:
            await page.wait_for_selector("button.actionLinks.js-viewModelDetails-modal",timeout=10000)
        except:
            pass

        try:
            await page.wait_for_selector("button.js-showUnavailableFloorPlansButton",timeout=10000)
            await page.locator("button.js-showUnavailableFloorPlansButton").first.click()
            await page.wait_for_selector("button.actionLinks.js-viewModelDetails-modal",timeout=10000)
        except:
            pass

        tree = HTMLParser(await page.content())
        roomTypesCounted = []
        urlsToAdd = []
        tempUrls = []

        roomInfo = tree.css("button.actionLinks.js-viewModelDetails-modal")
        for room in roomInfo:
            roomType = room.attributes.get("data-rentalkey")

            if roomType not in roomTypesCounted:
                tempUrls.append(room.attributes.get("data-rentalkey") + "-1-floorPlan")
                roomTypesCounted.append(roomType)
        
        for tempUrl in tempUrls:
            urlsToAdd.append(url + "#" + tempUrl)

        await page.close()
        return urlsToAdd

async def getFinalUrls(urls, browser):
    finalUrls = {}
    for url in urls:
        finalUrls[url] = await getUrls(url, browser)
    return finalUrls

async def getAllUrls(baseUrl, browser):
    urls = await getWebsiteUrls(baseUrl, browser)
    return await getFinalUrls(urls, browser)