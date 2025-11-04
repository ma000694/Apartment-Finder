import httpx
from selectolax.parser import HTMLParser
from getUrls import getUrls
from getAmenities import getAmenities, getDetails

def getInfo():
    urlDict = getUrls()
    infoDict = {}
    headers = {"User-Agent":"iTunes/12.13 (Windows; Microsoft Windows 10 x64; x64) AppleWebKit/7613.2007"}

    for apartUrl, urls in urlDict.items():
        resp = httpx.get(apartUrl, headers=headers)
        html = HTMLParser(resp.text)
        apartmentInfo = []

        apartmentName = html.css_first("h1#propertyName.propertyName").text()
        apartmentInfo.append(html.css_first("span.delivery-address").text().strip() + html.css_first("span.stateZipContainer").text().strip())

        for url in urls:
            if getAmenities(url) is not None:
                apartmentInfo.append(getDetails(url))
                apartmentInfo.append(getAmenities(url))
            
        infoDict[apartmentName] = apartmentInfo

    return infoDict

        
