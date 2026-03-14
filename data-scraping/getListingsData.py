import time, asyncio, os
from selectolax.parser import HTMLParser # HTML -> HTML Tree
from playwright.async_api import async_playwright # browser automation
from playwright_stealth import Stealth

# launch browser, scrapes all listing URLs, returns as dictionary of property link and their listings
async def getData(url):

    # dictionary to store property link (key), and listings (values).
    infoDict = {}

    # create async function, launches firefox (instead of Chrome) to scrape.
    # async with async_playwright() as p:
    async with async_playwright() as p:
        # browser = await p.firefox.launch(headless=False) # launch the browser
        browser = await p.chromium.launch(headless=True)

        # extracts urls from pages
        urls = await getUrls(url, browser)
        # houses
#        urls = ['https://listings.umn.edu/city/minneapolis-mn/listing/43517', 'https://listings.umn.edu/city/minneapolis-mn/listing/111850', 'https://listings.umn.edu/city/minneapolis-mn/listing/110628', 'https://listings.umn.edu/city/minneapolis-mn/listing/38224', 'https://listings.umn.edu/city/minneapolis-mn/listing/83458', 'https://listings.umn.edu/city/minneapolis-mn/listing/9591', 'https://listings.umn.edu/city/minneapolis-mn/listing/9715', 'https://listings.umn.edu/city/minneapolis-mn/listing/9588', 'https://listings.umn.edu/city/minneapolis-mn/listing/70922', 'https://listings.umn.edu/city/minneapolis-mn/listing/58534', 'https://listings.umn.edu/city/minneapolis-mn/listing/116188', 'https://listings.umn.edu/city/minneapolis-mn/listing/230525', 'https://listings.umn.edu/city/minneapolis-mn/listing/78760', 'https://listings.umn.edu/city/minneapolis-mn/listing/38176', 'https://listings.umn.edu/city/minneapolis-mn/listing/232982', 'https://listings.umn.edu/city/minneapolis-mn/listing/234813', 'https://listings.umn.edu/city/minneapolis-mn/listing/9594', 'https://listings.umn.edu/city/minneapolis-mn/listing/9579', 'https://listings.umn.edu/city/minneapolis-mn/listing/9573', 'https://listings.umn.edu/city/minneapolis-mn/listing/58517', 'https://listings.umn.edu/city/minneapolis-mn/listing/115164', 'https://listings.umn.edu/city/minneapolis-mn/listing/43657', 'https://listings.umn.edu/city/minneapolis-mn/listing/38223', 'https://listings.umn.edu/city/minneapolis-mn/listing/115167', 'https://listings.umn.edu/city/minneapolis-mn/listing/9600', 'https://listings.umn.edu/city/minneapolis-mn/listing/58529', 'https://listings.umn.edu/city/minneapolis-mn/listing/26357', 'https://listings.umn.edu/city/minneapolis-mn/listing/54284', 'https://listings.umn.edu/city/minneapolis-mn/listing/9555', 'https://listings.umn.edu/city/minneapolis-mn/listing/104426', 'https://listings.umn.edu/city/minneapolis-mn/listing/9553', 'https://listings.umn.edu/city/minneapolis-mn/listing/38217', 'https://listings.umn.edu/city/minneapolis-mn/listing/117691', 'https://listings.umn.edu/city/minneapolis-mn/listing/9561', 'https://listings.umn.edu/city/minneapolis-mn/listing/9554', 'https://listings.umn.edu/city/minneapolis-mn/listing/233113', 'https://listings.umn.edu/city/minneapolis-mn/listing/78758', 'https://listings.umn.edu/city/minneapolis-mn/listing/9556', 'https://listings.umn.edu/city/minneapolis-mn/listing/117510', 'https://listings.umn.edu/city/minneapolis-mn/listing/58525', 'https://listings.umn.edu/city/minneapolis-mn/listing/83714', 'https://listings.umn.edu/city/minneapolis-mn/listing/233760', 'https://listings.umn.edu/city/minneapolis-mn/listing/108646', 'https://listings.umn.edu/city/minneapolis-mn/listing/234817', 'https://listings.umn.edu/city/minneapolis-mn/listing/9549', 'https://listings.umn.edu/city/minneapolis-mn/listing/233114', 'https://listings.umn.edu/city/minneapolis-mn/listing/9560', 'https://listings.umn.edu/city/minneapolis-mn/listing/233759', 'https://listings.umn.edu/city/minneapolis-mn/listing/26333', 'https://listings.umn.edu/city/minneapolis-mn/listing/67366', 'https://listings.umn.edu/city/minneapolis-mn/listing/70441', 'https://listings.umn.edu/city/minneapolis-mn/listing/58543', 'https://listings.umn.edu/city/minneapolis-mn/listing/115165', 'https://listings.umn.edu/city/minneapolis-mn/listing/234812', 'https://listings.umn.edu/city/minneapolis-mn/listing/9551', 'https://listings.umn.edu/city/minneapolis-mn/listing/9584', 'https://listings.umn.edu/city/minneapolis-mn/listing/71323', 'https://listings.umn.edu/city/minneapolis-mn/listing/9592', 'https://listings.umn.edu/city/minneapolis-mn/listing/48486', 'https://listings.umn.edu/city/minneapolis-mn/listing/9576', 'https://listings.umn.edu/city/minneapolis-mn/listing/9577', 'https://listings.umn.edu/city/minneapolis-mn/listing/72176', 'https://listings.umn.edu/city/minneapolis-mn/listing/9569', 'https://listings.umn.edu/city/minneapolis-mn/listing/78613', 'https://listings.umn.edu/city/minneapolis-mn/listing/43225', 'https://listings.umn.edu/city/minneapolis-mn/listing/9590', 'https://listings.umn.edu/city/minneapolis-mn/listing/58535', 'https://listings.umn.edu/city/minneapolis-mn/listing/233112', 'https://listings.umn.edu/city/minneapolis-mn/listing/43518', 'https://listings.umn.edu/city/minneapolis-mn/listing/26358', 'https://listings.umn.edu/city/minneapolis-mn/listing/9583', 'https://listings.umn.edu/city/minneapolis-mn/listing/43822', 'https://listings.umn.edu/city/minneapolis-mn/listing/85044', 'https://listings.umn.edu/city/minneapolis-mn/listing/9568', 'https://listings.umn.edu/city/minneapolis-mn/listing/83459', 'https://listings.umn.edu/city/minneapolis-mn/listing/234816', 'https://listings.umn.edu/city/minneapolis-mn/listing/62030', 'https://listings.umn.edu/city/minneapolis-mn/listing/9593', 'https://listings.umn.edu/city/minneapolis-mn/listing/68344', 'https://listings.umn.edu/city/minneapolis-mn/listing/232765', 'https://listings.umn.edu/city/minneapolis-mn/listing/9571', 'https://listings.umn.edu/city/minneapolis-mn/listing/115296', 'https://listings.umn.edu/city/minneapolis-mn/listing/77017', 'https://listings.umn.edu/city/minneapolis-mn/listing/70959', 'https://listings.umn.edu/city/minneapolis-mn/listing/9557', 'https://listings.umn.edu/city/minneapolis-mn/listing/9565', 'https://listings.umn.edu/city/minneapolis-mn/listing/43655', 'https://listings.umn.edu/city/minneapolis-mn/listing/115163', 'https://listings.umn.edu/city/minneapolis-mn/listing/58527', 'https://listings.umn.edu/city/minneapolis-mn/listing/43213', 'https://listings.umn.edu/city/minneapolis-mn/listing/43215', 'https://listings.umn.edu/city/minneapolis-mn/listing/234814', 'https://listings.umn.edu/city/minneapolis-mn/listing/231036', 'https://listings.umn.edu/city/minneapolis-mn/listing/43656', 'https://listings.umn.edu/city/minneapolis-mn/listing/230640', 'https://listings.umn.edu/city/minneapolis-mn/listing/100062', 'https://listings.umn.edu/city/minneapolis-mn/listing/234815']
        # apartments
#        urls = ['https://listings.umn.edu/city/minneapolis-mn/listing/44172', 'https://listings.umn.edu/city/minneapolis-mn/listing/10044', 'https://listings.umn.edu/city/minneapolis-mn/listing/115626', 'https://listings.umn.edu/city/minneapolis-mn/listing/76215', 'https://listings.umn.edu/city/minneapolis-mn/listing/11676', 'https://listings.umn.edu/city/minneapolis-mn/listing/9714', 'https://listings.umn.edu/city/minneapolis-mn/listing/11393', 'https://listings.umn.edu/city/minneapolis-mn/listing/60211', 'https://listings.umn.edu/city/minneapolis-mn/listing/10057', 'https://listings.umn.edu/city/minneapolis-mn/listing/230892', 'https://listings.umn.edu/city/minneapolis-mn/listing/10036', 'https://listings.umn.edu/city/minneapolis-mn/listing/10041', 'https://listings.umn.edu/city/minneapolis-mn/listing/10336', 'https://listings.umn.edu/city/minneapolis-mn/listing/9548', 'https://listings.umn.edu/city/minneapolis-mn/listing/229984', 'https://listings.umn.edu/city/minneapolis-mn/listing/69586', 'https://listings.umn.edu/city/minneapolis-mn/listing/112484', 'https://listings.umn.edu/city/minneapolis-mn/listing/10058', 'https://listings.umn.edu/city/minneapolis-mn/listing/26283', 'https://listings.umn.edu/city/minneapolis-mn/listing/9727', 'https://listings.umn.edu/city/minneapolis-mn/listing/58442', 'https://listings.umn.edu/city/minneapolis-mn/listing/117997', 'https://listings.umn.edu/city/minneapolis-mn/listing/11391', 'https://listings.umn.edu/city/minneapolis-mn/listing/11394', 'https://listings.umn.edu/city/minneapolis-mn/listing/26507', 'https://listings.umn.edu/city/minneapolis-mn/listing/70274', 'https://listings.umn.edu/city/minneapolis-mn/listing/10051', 'https://listings.umn.edu/city/minneapolis-mn/listing/10052', 'https://listings.umn.edu/city/minneapolis-mn/listing/231299', 'https://listings.umn.edu/city/minneapolis-mn/listing/101114', 'https://listings.umn.edu/city/minneapolis-mn/listing/57528', 'https://listings.umn.edu/city/minneapolis-mn/listing/9597', 'https://listings.umn.edu/city/minneapolis-mn/listing/75746', 'https://listings.umn.edu/city/minneapolis-mn/listing/26284', 'https://listings.umn.edu/city/minneapolis-mn/listing/26355', 'https://listings.umn.edu/city/minneapolis-mn/listing/67375', 'https://listings.umn.edu/city/minneapolis-mn/listing/83278', 'https://listings.umn.edu/city/minneapolis-mn/listing/26327', 'https://listings.umn.edu/city/minneapolis-mn/listing/49181', 'https://listings.umn.edu/city/minneapolis-mn/listing/38278', 'https://listings.umn.edu/city/minneapolis-mn/listing/78192', 'https://listings.umn.edu/city/minneapolis-mn/listing/43710', 'https://listings.umn.edu/city/minneapolis-mn/listing/78143', 'https://listings.umn.edu/city/minneapolis-mn/listing/78208', 'https://listings.umn.edu/city/minneapolis-mn/listing/38192', 'https://listings.umn.edu/city/minneapolis-mn/listing/70804', 'https://listings.umn.edu/city/minneapolis-mn/listing/26356', 'https://listings.umn.edu/city/minneapolis-mn/listing/108389', 'https://listings.umn.edu/city/minneapolis-mn/listing/38181', 'https://listings.umn.edu/city/minneapolis-mn/listing/26286', 'https://listings.umn.edu/city/minneapolis-mn/listing/53326', 'https://listings.umn.edu/city/minneapolis-mn/listing/230083', 'https://listings.umn.edu/city/minneapolis-mn/listing/9730', 'https://listings.umn.edu/city/minneapolis-mn/listing/83279', 'https://listings.umn.edu/city/minneapolis-mn/listing/110910', 'https://listings.umn.edu/city/minneapolis-mn/listing/229867', 'https://listings.umn.edu/city/minneapolis-mn/listing/10020', 'https://listings.umn.edu/city/minneapolis-mn/listing/43711', 'https://listings.umn.edu/city/minneapolis-mn/listing/27244', 'https://listings.umn.edu/city/minneapolis-mn/listing/78117', 'https://listings.umn.edu/city/minneapolis-mn/listing/9710', 'https://listings.umn.edu/city/minneapolis-mn/listing/43987', 'https://listings.umn.edu/city/minneapolis-mn/listing/78131', 'https://listings.umn.edu/city/minneapolis-mn/listing/10335', 'https://listings.umn.edu/city/minneapolis-mn/listing/9581', 'https://listings.umn.edu/city/minneapolis-mn/listing/234876', 'https://listings.umn.edu/city/minneapolis-mn/listing/54316', 'https://listings.umn.edu/city/minneapolis-mn/listing/53057', 'https://listings.umn.edu/city/minneapolis-mn/listing/69882', 'https://listings.umn.edu/city/minneapolis-mn/listing/58177', 'https://listings.umn.edu/city/minneapolis-mn/listing/12634', 'https://listings.umn.edu/city/minneapolis-mn/listing/43990', 'https://listings.umn.edu/city/minneapolis-mn/listing/114866', 'https://listings.umn.edu/city/minneapolis-mn/listing/43847', 'https://listings.umn.edu/city/minneapolis-mn/listing/229981', 'https://listings.umn.edu/city/minneapolis-mn/listing/96574', 'https://listings.umn.edu/city/minneapolis-mn/listing/9716', 'https://listings.umn.edu/city/minneapolis-mn/listing/26482', 'https://listings.umn.edu/city/minneapolis-mn/listing/229982', 'https://listings.umn.edu/city/minneapolis-mn/listing/233489', 'https://listings.umn.edu/city/minneapolis-mn/listing/9720', 'https://listings.umn.edu/city/minneapolis-mn/listing/26480', 'https://listings.umn.edu/city/minneapolis-mn/listing/9713', 'https://listings.umn.edu/city/minneapolis-mn/listing/100719', 'https://listings.umn.edu/city/minneapolis-mn/listing/113221', 'https://listings.umn.edu/city/minneapolis-mn/listing/38182', 'https://listings.umn.edu/city/minneapolis-mn/listing/61964', 'https://listings.umn.edu/city/minneapolis-mn/listing/10065', 'https://listings.umn.edu/city/minneapolis-mn/listing/78141', 'https://listings.umn.edu/city/minneapolis-mn/listing/43717', 'https://listings.umn.edu/city/minneapolis-mn/listing/51564', 'https://listings.umn.edu/city/minneapolis-mn/listing/78111', 'https://listings.umn.edu/city/minneapolis-mn/listing/68225', 'https://listings.umn.edu/city/minneapolis-mn/listing/26484', 'https://listings.umn.edu/city/minneapolis-mn/listing/114868', 'https://listings.umn.edu/city/minneapolis-mn/listing/114588', 'https://listings.umn.edu/city/minneapolis-mn/listing/9717', 'https://listings.umn.edu/city/minneapolis-mn/listing/102817', 'https://listings.umn.edu/city/minneapolis-mn/listing/38194', 'https://listings.umn.edu/city/minneapolis-mn/listing/50255', 'https://listings.umn.edu/city/minneapolis-mn/listing/10042', 'https://listings.umn.edu/city/minneapolis-mn/listing/9552', 'https://listings.umn.edu/city/minneapolis-mn/listing/38027', 'https://listings.umn.edu/city/minneapolis-mn/listing/12635', 'https://listings.umn.edu/city/minneapolis-mn/listing/83289', 'https://listings.umn.edu/city/minneapolis-mn/listing/10010', 'https://listings.umn.edu/city/minneapolis-mn/listing/68224', 'https://listings.umn.edu/city/minneapolis-mn/listing/62115', 'https://listings.umn.edu/city/minneapolis-mn/listing/43709', 'https://listings.umn.edu/city/minneapolis-mn/listing/67926', 'https://listings.umn.edu/city/minneapolis-mn/listing/108867', 'https://listings.umn.edu/city/minneapolis-mn/listing/10046', 'https://listings.umn.edu/city/minneapolis-mn/listing/43707', 'https://listings.umn.edu/city/minneapolis-mn/listing/50251', 'https://listings.umn.edu/city/minneapolis-mn/listing/230084', 'https://listings.umn.edu/city/minneapolis-mn/listing/10048', 'https://listings.umn.edu/city/minneapolis-mn/listing/43222', 'https://listings.umn.edu/city/minneapolis-mn/listing/43716', 'https://listings.umn.edu/city/minneapolis-mn/listing/43988', 'https://listings.umn.edu/city/minneapolis-mn/listing/105202', 'https://listings.umn.edu/city/minneapolis-mn/listing/26481', 'https://listings.umn.edu/city/minneapolis-mn/listing/53325', 'https://listings.umn.edu/city/minneapolis-mn/listing/11395', 'https://listings.umn.edu/city/minneapolis-mn/listing/229983', 'https://listings.umn.edu/city/minneapolis-mn/listing/43706', 'https://listings.umn.edu/city/minneapolis-mn/listing/10049', 'https://listings.umn.edu/city/minneapolis-mn/listing/78108', 'https://listings.umn.edu/city/minneapolis-mn/listing/10359', 'https://listings.umn.edu/city/minneapolis-mn/listing/13798', 'https://listings.umn.edu/city/minneapolis-mn/listing/43715', 'https://listings.umn.edu/city/minneapolis-mn/listing/9718', 'https://listings.umn.edu/city/minneapolis-mn/listing/38026', 'https://listings.umn.edu/city/minneapolis-mn/listing/10043', 'https://listings.umn.edu/city/minneapolis-mn/listing/104176', 'https://listings.umn.edu/city/minneapolis-mn/listing/26324', 'https://listings.umn.edu/city/minneapolis-mn/listing/26483', 'https://listings.umn.edu/city/minneapolis-mn/listing/231298', 'https://listings.umn.edu/city/minneapolis-mn/listing/115159', 'https://listings.umn.edu/city/minneapolis-mn/listing/43718', 'https://listings.umn.edu/city/minneapolis-mn/listing/78110', 'https://listings.umn.edu/city/minneapolis-mn/listing/43708', 'https://listings.umn.edu/city/minneapolis-mn/listing/73572', 'https://listings.umn.edu/city/minneapolis-mn/listing/113389', 'https://listings.umn.edu/city/minneapolis-mn/listing/104427', 'https://listings.umn.edu/city/minneapolis-mn/listing/9578', 'https://listings.umn.edu/city/minneapolis-mn/listing/111072', 'https://listings.umn.edu/city/minneapolis-mn/listing/55720', 'https://listings.umn.edu/city/minneapolis-mn/listing/39087', 'https://listings.umn.edu/city/minneapolis-mn/listing/54620', 'https://listings.umn.edu/city/minneapolis-mn/listing/10063', 'https://listings.umn.edu/city/minneapolis-mn/listing/70588', 'https://listings.umn.edu/city/minneapolis-mn/listing/76812', 'https://listings.umn.edu/city/minneapolis-mn/listing/78118', 'https://listings.umn.edu/city/minneapolis-mn/listing/102810', 'https://listings.umn.edu/city/minneapolis-mn/listing/84713', 'https://listings.umn.edu/city/minneapolis-mn/listing/61953', 'https://listings.umn.edu/city/minneapolis-mn/listing/115126', 'https://listings.umn.edu/city/minneapolis-mn/listing/43991']
        
        # prints for debugging
        print(urls)

        # iterate each url, extract HTML to create queryable tree, to extract address, title (name), info, and amenities. 
        for url in urls:
            try:
                timeStart = time.time()
                html = await goTo(browser, url)
                tree = HTMLParser(html)

                address = await getAddress(tree)
                title = await getTitle(tree)
                info = await getInfo(tree)
                amenities = [', '.join(await getAmenities(tree))]
#                amenities = await getAmenities(tree)
            
                # if property name not in dict, add into dict to add values
                if title not in infoDict:
                    infoDict[title] = {}
                
                # iterate through info to unpack listing info (name, bed, baths, etc...)
                for key in info:
                    name, beds, baths, rent, sqft, availability = info[key]
                    data = [address, beds, baths, rent, sqft, availability, url]
                    data.extend(amenities)
                    infoDict[title][name] = data
                print(f"Completed {url} in {(time.time() - timeStart):.2f} seconds.")
            except Exception as e:
                print(f"Error processing {url} on {e}")

    # return dictionary
    return infoDict

# loads listing page, 5 tries, and introduce CAPTCHA... manual process
async def goTo(browser, url):

    # loads page, 5 tries...
    for _ in range(5):

        # for CAPTCHA tracking
        pause = False

        # loads page
        try:
            page = await browser.new_page()
            await Stealth().apply_stealth_async(page)  # applying stealth before navigation

            page.set_default_timeout(60000)  # 60 seconds
            response = await page.goto(url, wait_until="networkidle")
            html = await page.content()
            
            # CAPTCHA catch
            if "Access Denied" in html or response.status != 200:
                print("Complete CAPTCHA.")

                # pause, awaiting manual CAPTCHA
                await page.pause()
                await page.wait_for_timeout(5000)  # wait for 5 seconds

                # update CAPTCHA track
                pause = True

                # extract HTML
                html = await page.content()
            
            # close page
            await page.close()
            if pause:
                time.sleep(10)
            break
        except Exception as e:
            print(f"Failed to load {url} on {e}")
            try:
                await page.close()
            except:
                pass
            time.sleep(5)

    # return loose HTML
    return html

# loads listing page, clicks through all listing, and extract list of individual listings' URL. 
async def getUrls(url, browser):

    # loads page, 5 tries
    for _ in range(5):

        # load page
        try:
            page = await browser.new_page()
            await Stealth().apply_stealth_async(page)  # applying stealth before navigation

            page.set_default_timeout(60000)  # 60 seconds
            response = await page.goto(url, wait_until="networkidle")
            html = await page.content()

            # CAPTCHA catch
            if "Access Denied" in html or response.status != 200:
                print("Complete CAPTCHA.")
                await page.pause()
                await page.wait_for_timeout(1000)  # wait for 1 seconds
                html = await page.content()
        except Exception as e:
            print(f"Error loading {url} on {e}")
            await page.close()
            time.sleep(10)
        if not("Access Denied" in html or response.status != 200):
            break

    # scroll infinitely to load pages.
    try:
        while await page.locator("div.c-list").count() > 0:
            await page.click("div.col-sm-10")
            await page.wait_for_load_state("networkidle")
    except:
        pass
    
    # extract HTML, parsed to create queryable tree
    html = await page.content()
    tree = HTMLParser(html)

    # close
    await page.close()

    # store listing IDs from site
    ids = []

    # finds all listings, return as list, append id into id list
    try:
        nodes = tree.css("div.c-list")
        for node in nodes:
            ids.append(node.attributes['data-property-id'])
    except Exception as e:
        print(f"Error getting urls on {e}")
    
    # store listing urls.
    urls = []

    # iterate through id and append listing url, with format below. 
    for id in ids:
        urls.append(f"https://listings.umn.edu/city/minneapolis-mn/listing/{id}")

    # print size of list, and return list
    print(len(urls))
    return urls

# extracts property address, and clean string
async def getAddress(tree):
    try:
        address = tree.css_first("span.sub-heading").text().strip().replace("\n","").replace("  ","").replace(",","").replace("SEM", "SE M").replace("StM", "St M").replace("MN5", "MN 5").replace("SMin", "S Min")
    except:
        address = "Address not found"
    return address

# extracts property name, and clean string
async def getTitle(tree):
    try:
        title = tree.css_first("div.col-md-12.col-lg-4.headingCampus-detailSec h1").text().strip().replace("\n","").replace("  ","").replace(",","")
    except:
        title = "Title not found"
    return title

# extracts property info and store/return list
async def getInfo(tree):
    info = {}
    try:
        table = tree.css_first("table.table-overflow")
        nodes = table.css("tbody tr")
        for i, node in enumerate(nodes):
            data = node.css("td")
            dataText = []
            for dp in data:
                dpText = dp.text().strip().replace("\n","").replace("  ","").replace(",","")
                dataText.append(dpText)
            info[i] = dataText
    except:
        info = {"not found": ["not found","not found","not found","not found"]}
    return info

# extract property amenities and store/return list
async def getAmenities(tree):
    amenities = []
    try:
        nodes = tree.css("div.feature-block.row-extra div#accordion div div ul li")
        for node in nodes:
            amenity = node.text().strip().replace("\n","").replace("  ","").replace(",","")
            amenities.append(amenity)
    except:
        amenities = ["Amenities not found"]
    return amenities

# takes scraped data, and create CSV file from data.
async def makeCSV(data, filename):
    import csv

    # output into csv folder, instead data-scraping
    os.makedirs("scaped-csv", exist_ok= True) # if exist, continue, else create

    filepath = os.path.join("scraped-csv", filename) # build filepath

    # open/overwrite file, and write data, using format
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        header = ["Building Name", "Unit Name", "Address", "Beds", "Baths", "Rent", "Sqft", "Availability", "URL", "Amenities"]
        writer.writerow(header)

        for title in data:
            for unit in data[title]:
                row = [title, unit]
                row.extend(data[title][unit])
                writer.writerow(row)

if __name__ == "__main__":
    time_start = time.time()

    housingData = asyncio.run(getData("https://listings.umn.edu/listing?category=19%2C29"))
    asyncio.run(makeCSV(housingData, "umn_housing_data.csv"))
    time_finish = time.time()
    print(f"House data extraction completed in {(time_finish - time_start):.2f} seconds.")

    apartmentData = asyncio.run(getData("https://listings.umn.edu/listing?category=15"))
    asyncio.run(makeCSV(apartmentData, "umn_apartment_data.csv"))
    print(f"Apartment data extraction completed in {(time.time() - time_start):.2f}")


# I want to create a feature that allows the async function to bypass captcha, currently we have to manually solve captcha.
# I could try and use playwright_stealth, which should theoretically bypass captcha, but making the page believe the browser is an actual user.
# Currently this program uses async_playwright, which creates an async browser.
# If I replaced this using stealth this should work?