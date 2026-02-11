import time, asyncio
from playwright.async_api import async_playwright
from getUrls import getAllUrls
from getAmenities import getAmenities, getDetails, getRent, getRoomType, getContent, getPropertyUrl, getPageContent, getNameAndAddress

async def getInfo():
    urlDict = {}
    infoDict = {}
    neighborhoodsMN = ["https://www.apartments.com/apartments/dinkytown-minneapolis-mn/?n=prospect-park_minneapolis_mn+west-bank_minneapolis_mn+como_minneapolis_mn",
                       "https://www.apartments.com/apartments/dinkytown-minneapolis-mn/2/?n=prospect-park_minneapolis_mn+west-bank_minneapolis_mn+como_minneapolis_mn",
                       "https://www.apartments.com/apartments/dinkytown-minneapolis-mn/3/?n=prospect-park_minneapolis_mn+west-bank_minneapolis_mn+como_minneapolis_mn"]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, timeout=0)
        
        for neighborhood in neighborhoodsMN: # build a list of all of the urls to parse through, right now they correspond to the apartments in these zip codes: 55414, 55454, 55455
            urlDict.update(await getAllUrls(neighborhood, browser))

        for apartUrl, urls in urlDict.items():
            apartmentInfo = []
            if not urls:
                continue
            pageHtml = await getPageContent(apartUrl, browser)
            nameAndAddress = getNameAndAddress(pageHtml)

            for url in urls: # gets the info for every room in the property
                start = time.perf_counter()
                html = await getContent(url, browser)
                if getAmenities(html) is not None:
                    apartmentInfo.extend(nameAndAddress)
                    apartmentInfo.append(getRoomType(html))
                    apartmentInfo.append(getRent(html))
                    apartmentInfo.extend(getDetails(html))
                    apartmentInfo.append(getPropertyUrl(html))
                    apartmentInfo.extend(getAmenities(html))
                    apartmentInfo.append("\n")
                    print(f"elapsed time: {(time.perf_counter() - start):.4f} seconds")
                
            infoDict[nameAndAddress[0]] = apartmentInfo # returns a dictionary where the keys are the name of the property and the values is the info of the property
        await browser.close()
    return infoDict


async def makeFile():
    startTime = time.perf_counter()
    infoDict = await getInfo()

    with open("apartmentInfo.csv", "w") as fp:
        for aptinfo in infoDict.values(): # build a csv file with each room in each property having its own line
            fp.write(",")
            fp.write(",".join(aptinfo))

    endTime = time.perf_counter()
    print(f"Program executed in {(endTime - startTime):.4f} seconds")

if __name__ == "__main__":
    asyncio.run(makeFile())
