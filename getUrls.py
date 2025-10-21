import httpx
from selectolax.parser import HTMLParser

def getUrls():
    BasewebsiteUrl = "https://www.apartments.com/off-campus-housing/mn/minneapolis/university-of-minnesota/student-housing-per-person/"
    headers = {"User-Agent":"iTunes/12.13 (Windows; Microsoft Windows 10 x64; x64) AppleWebKit/7613.2007"}

    websiteUrls = [BasewebsiteUrl]
    i = 1
    while(i <= 18):
        websiteUrls.append(BasewebsiteUrl + f"{i}/")
        i += 1

    urls = []

    for websiteUrl in websiteUrls:
        resp = httpx.get(websiteUrl, headers=headers, timeout=10)
        html = HTMLParser(resp.text)

        apartments = html.css("a.property-link")

        for apartment in apartments:
            url = apartment.attributes.get("href")
            if url is not None:
                urls.append(url)

    return urls
