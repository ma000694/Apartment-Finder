import httpx
from selectolax.parser import HTMLParser


url = "https://www.apartments.com/holden-house-saint-paul-mn/dmxeevk/"
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15"}
resp = httpx.get(url, headers=headers, verify=False)
html = HTMLParser(resp.text)

prices = html.css("div.mortar-wrapper ul li") #grabbing all of the prices

my_list = []

for price in prices:
    my_list.append(price.text().strip().replace("\n", "").replace("\t", "").replace("  ", ""))
#print(my_list[4])

url2 = "https://www.apartments.com/holden-house-saint-paul-mn/dmxeevk/#p2tptes-2-unit"
resp2 = httpx.get(url2, headers=headers, verify=False)
html2 = HTMLParser(resp2.text)
rentals = html2.css("ul.allAmenities ul li")

for rental in rentals:
    print(rental.text())
