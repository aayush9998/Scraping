import requests
from bs4 import BeautifulSoup as soup
from selenium import webdriver

# searchdaraz = request.POST.get('searchdaraz')
    # driver = webdriver.Chrome('E:\chromedriver_win32/chromedriver')
driver = webdriver.Chrome('D:\office/chromedriver')
# driver = get_driver()

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)



baseurl = "https://www.daraz.com.np/catalog/?q=Laptop"
# def getlaps(page):
# for x in range(1, 3):
driver.get(baseurl)

productlink = []

page = driver.page_source
page = driver.execute_script("return document.documentElement.outerHTML")

pg_soup = soup(page, "lxml")

contain = pg_soup.findAll("div", {"class": "c5TXIP"})

for items in contain:
    item = items.find('div', {"class": "c16H9d"})
    for link in item.findAll('a', href=True):
        item_link = "https:" + link['href']
        print(item_link)
        productlink.append(item_link)

for link in productlink:
    driver.get(link)
    page = driver.page_source
    pg_soup = soup(page, "lxml")

    brand = pg_soup.find('a', {
        'class': 'pdp-link pdp-link_size_s pdp-link_theme_blue pdp-product-brand__brand-link'}).text
    title = pg_soup.find('span', {'class': 'pdp-mod-product-badge-title'}).text
    price = pg_soup.find('span', {
        'class': 'pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl'}).text
    category = pg_soup.findAll('a', attrs={'class': 'breadcrumb_item_anchor'})[2]['title']
    try:
        orginal = pg_soup.find('span', {
            'class': 'pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs'}).text
        discount = pg_soup.find('span', {'class': 'pdp-product-price__discount'}).text
    except:
        orginal = pg_soup.find('span', {
            'class': 'pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl'}).text
        discount = 'no discount'

    print(brand, title, price, category, orginal,discount)
#     Daraz.objects.create(brand =brand,
#                 title= title,
#                 price= price,
#                 category= category,
#                 original= orginal,
#                 discount= discount,)
# return redirect(scrape)