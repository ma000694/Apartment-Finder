import time, asyncio

# third-party libraries
from playwright.async_api import async_playwright # import browser automation library, for Chrome, using async version.
from getUrls import getAllUrls # function from file getUrls.py -- handles URL discovery.
from getAmenities import getAmenities, getDetails, getRent, getRoomType, getContent, getPropertyUrl, getPageContent, getNameAndAddress # functions from getAmenities, handles data-extraction from url.

# async function, that extracts listing information
async def getInfo():
    # map for viewed listings
    urlDict = {}
    # map for listing and their amenities
    infoDict = {}
    # where we are extracting information from
    neighborhoodsMN = ["https://www.apartments.com/apartments/dinkytown-minneapolis-mn/?n=prospect-park_minneapolis_mn+west-bank_minneapolis_mn+como_minneapolis_mn",
                    "https://www.apartments.com/apartments/dinkytown-minneapolis-mn/2/?n=prospect-park_minneapolis_mn+west-bank_minneapolis_mn+como_minneapolis_mn",
                    "https://www.apartments.com/apartments/dinkytown-minneapolis-mn/3/?n=prospect-park_minneapolis_mn+west-bank_minneapolis_mn+como_minneapolis_mn"]
    # TODO: These doesn't include some key locations such as Identity, Standard, and the Brownstones.

    # creates a browser instances, that surfs each links and extract information
    async with async_playwright() as p:

        # creates browser instances, with active window, and removes timeout.
        browser = await p.chromium.launch(headless=False, timeout=0)
        
        # loops through each link
        for neighborhood in neighborhoodsMN: # build a list of all of the urls to parse through, right now they correspond to the apartments in these zip codes: 55414, 55454, 55455
            
            # creates map of properties and their individual listings, used below
            urlDict.update(await getAllUrls(neighborhood, browser))

        # loops through map from above, and index through property url and listings url.
        for apartUrl, urls in urlDict.items():

            # will be used to store amenities
            apartmentInfo = []

            # if property have no listings, skip.
            if not urls:
                continue

            # extracts the HTML of the property site
            pageHtml = await getPageContent(apartUrl, browser)

            # extracts the name and address from HTML
            nameAndAddress = getNameAndAddress(pageHtml)

            # loops through each listing urls
            for url in urls: # gets the info for every room in the property

                # records duration to access url, spotting slow pages...
                start = time.perf_counter()

                # extract html from url
                html = await getContent(url, browser)

                # if there are amenities, add into list
                if getAmenities(html) is not None:
                    apartmentInfo.extend(nameAndAddress)
                    apartmentInfo.append(getRoomType(html))
                    apartmentInfo.append(getRent(html))
                    apartmentInfo.extend(getDetails(html))
                    apartmentInfo.append(getPropertyUrl(html))
                    apartmentInfo.extend(getAmenities(html))
                    apartmentInfo.append("\n")
                    print(f"elapsed time: {(time.perf_counter() - start):.4f} seconds")
            
            # stores list of amenities into list
            infoDict[nameAndAddress[0]] = apartmentInfo # returns a dictionary where the keys are the name of the property and the values is the info of the property

        # close browser
        await browser.close()

    # return list of amenities
    return infoDict

# creates CSV file of listing and their info.
async def makeFile():
    
    # record duration
    startTime = time.perf_counter()

    # request updated listings with info from function above.
    infoDict = await getInfo()

    # creates/overwrites file called apartmentInfo.csv with apartment and their information
    with open("apartmentInfo.csv", "w") as fp:

        # iterate through apartment information, building file
        for aptinfo in infoDict.values(): # build a csv file with each room in each property having its own line
            fp.write(",") # might be redundant, but program works, so don't fix.
            fp.write(",".join(aptinfo)) # not redundant.

    # record duration
    endTime = time.perf_counter()
    print(f"Program executed in {(endTime - startTime):.4f} seconds")

if __name__ == "__main__":
    # starts async loop
    asyncio.run(makeFile())
