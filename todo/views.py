import requests
import os
# import grequests
from django.shortcuts import render, redirect
from .models import Daraz, SastoDeal, Hamrobazar
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from . import models
from requests.compat import quote_plus
# Create your views here.
#
# def get_driver():
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
#     driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
#
#     return driver

def index(request):
    # todo_items = Todo.objects.all()
    return render(request, 'index.html')

def scrape(request):
    # todo_items = Todo.objects.all()
    return render(request, 'scrape.html')


def search(request):
    if request.method == 'GET':
        todo_items = None
        sasto_item = None
        hamrobazar_item= None
        if request.GET.get('model'):
            search = request.GET.get('model')
            print("search:"+ search)
            
            if request.GET.get('darazcheck'):
                todo_items = Daraz.objects.filter(title__contains=search)

            if request.GET.get('sastodealcheck'):
                sasto_item = SastoDeal.objects.filter(title__contains=search)

            if request.GET.get('hamrobazarcheck'):
                hamrobazar_item = Hamrobazar.objects.filter(title__contains=search)

        return render(request, 'search.html', {'todo_items': todo_items, 'sasto_item': sasto_item, 'hamrobazar_item': hamrobazar_item})

def sastodeal_item(request):
    # SastoDeal.objects.all().delete()
    searchsasto= request.POST.get('searchsasto')
    # driver = webdriver.Chrome('E:\chromedriver_win32/chromedriver')
    driver = webdriver.Chrome('D:\office/chromedriver')
    # driver= get_driver()


    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    for x in range (1,3):
        baseurl = f'https://www.sastodeal.com/catalogsearch/result/index/?p={x}&q={searchsasto}'
        # baseurl = 'https://www.sastodeal.com/catalogsearch/result/?q={}'

        driver.get(baseurl.format(quote_plus(searchsasto)))

        productlink = []
        page = driver.page_source
        page = driver.execute_script("return document.documentElement.outerHTML")

        pg_soup = soup(page, "lxml")

        contain = pg_soup.findAll("div", {"class": "actions-primary"})

        for link in contain:
            item_link = link.a['href']
            item_title= link.a.text
            print(item_link)
            print(item_title)

            item_sasto = SastoDeal.objects.filter(title=item_title)
            if not item_sasto.exists():
                # productlink.append(link['href'])
            # print(productlink)

        # for links in productlink:
                driver.get(item_link)
                page = driver.page_source
                pg_soup = soup(page, "lxml")

                brand = pg_soup.find('span', {'class': 'col data'}).text
                title = pg_soup.find('span', {'class': 'base'}).text
                price = pg_soup.find('span', {'class': 'price'}).text
                # category = pg_soup.findAll('a', attrs={'class': 'breadcrumb_item_anchor'})[2]['title']
                try:
                    orginal = pg_soup.find('span', {'class': 'price-container price-final_price tax weee'}).text
                    discount = pg_soup.find('span', {'class': 'disPrice'}).text
                except:
                    orginal = pg_soup.find('span', {'class': 'price'}).text
                    discount = 'no discount'


                SastoDeal.objects.create(
                brand=brand,
                title=title,
                price=price,
                original=orginal,
                discount=discount,
                )

    return redirect(scrape)

def hamrobazar_item(request):
    # Hamrobazar.objects.all().delete()
    # driver = webdriver.Chrome('E:\chromedriver_win32/chromedriver')
    driver = webdriver.Chrome('D:\office/chromedriver')
    # driver= get_driver()
    baseurl = 'https://hamrobazaar.com/'
    driver.get(
        f'https://hamrobazaar.com/search.php?do_search=Search&searchword=laptops'
    )
    productlink = []
    page = driver.page_source
    page = driver.execute_script("return document.documentElement.outerHTML")

    pg_soup = soup(page, 'lxml')
    # print(soup)

    items = pg_soup.find_all('td', {'style': 'line:height:130%;'})
    for item in items:
        productlink.append(baseurl + item.a['href'])
    print(productlink)
    for link in productlink:
        driver.get(link)
        page = driver.page_source
        page = driver.execute_script("return document.documentElement.outerHTML")

        pg_soup = soup(page, 'lxml')

        title = pg_soup.find('span', {'class': 'title'}).text
        price = pg_soup.find('font', {'class': 'bigprice'}).text

        Hamrobazar.objects.create(
            title= title,
            price= price
        )

    return redirect(scrape)

def add_item(request):
    # Daraz.objects.all().delete()
    searchdaraz = request.POST.get('searchdaraz')
    # driver = webdriver.Chrome('E:\chromedriver_win32/chromedriver')
    driver = webdriver.Chrome('D:\office/chromedriver')
    # driver = get_driver()

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)



    # baseurl = "https://www.daraz.com.np/catalog/?q={}"
    for x in range (2,4):
        baseurl = f"https://www.daraz.com.np/catalog/?page={x}&q={searchdaraz}"
        driver.get(baseurl.format(quote_plus(searchdaraz)))

        # productlink = []

        page = driver.execute_script("return document.documentElement.outerHTML")

        pg_soup = soup(page, "lxml")

        # contain = pg_soup.findAll("div", {"class": "c5TXIP"})
        #
        # for items in contain:
        item = pg_soup.findAll('div', {"class": "c16H9d"})
        # print(item)
        # for link in item.findAll('a', href=True):
        for link in item:

            item_link = "https:" + link.a['href']
            item_title = link.a.text
            print(item_link)
            print(item_title)
            # productlink.append(item_link)

            item_daraz = Daraz.objects.filter(title=item_title)
            print(f'title does exist{item_daraz.exists()}\n')
            if not item_daraz.exists():
                driver.get(item_link)
                page = driver.page_source
                pg_soup = soup(page, "lxml")

                brand = pg_soup.find('a', {
                    'class': 'pdp-link pdp-link_size_s pdp-link_theme_blue pdp-product-brand__brand-link'}).text
                title = pg_soup.find('span', {'class': 'pdp-mod-product-badge-title'}).text
                price = pg_soup.find('span', {'class': 'pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl'}).text
                # category = pg_soup.findAll('a', attrs={'class': 'breadcrumb_item_anchor'})[2]['title']
                try:
                    orginal = pg_soup.find('span', {
                        'class': 'pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs'}).text
                    discount = pg_soup.find('span', {'class': 'pdp-product-price__discount'}).text
                except:
                    orginal = pg_soup.find('span', {
                        'class': 'pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl'}).text
                    discount = 'no discount'

                print(brand, title, price, orginal,discount)

                Daraz.objects.create(brand =brand,
                                title= title,
                                price= price,
                                # category= category,
                                original= orginal,
                                discount= discount,)

        # else:
        #     pk = item_daraz.first().id
        #     Daraz.objects.filter(id=pk).update(price=price,)
    return redirect(scrape)

