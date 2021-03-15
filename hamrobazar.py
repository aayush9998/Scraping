import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# raw_html = requests.get('https://hamrobazaar.com/c22-computer-and-peripherals-laptops?catid=22&order=popularad&offset=20').text
driver = webdriver.Chrome('E:\chromedriver_win32/chromedriver')
baseurl='https://hamrobazaar.com/'
driver.get(
    f'https://hamrobazaar.com/c22-computer-and-peripherals-laptops'
)

productlink = []
page = driver.page_source
page = driver.execute_script("return document.documentElement.outerHTML")

soup = BeautifulSoup(page, 'lxml')
# print(soup)

table_datas = soup.find_all('td',{'style': 'line:height:130%;' })
for table_data in table_datas:
    productlink.append(baseurl+ table_data.a['href'])
for link in productlink:
    driver.get(link)
    page = driver.page_source
    page = driver.execute_script("return document.documentElement.outerHTML")

    soup= BeautifulSoup(page, 'lxml')

    title= soup.find('span',{'class': 'title'}).text
    price= soup.find('font',{'class': 'bigprice'}).text
    laps={
        "title":title,
        "price":price,

    }
    print(laps)


