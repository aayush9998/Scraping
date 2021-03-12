from django.shortcuts import render, redirect
from .models import Daraz, SastoDeal
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from . import models
# Create your views here.


def index(request):
    # todo_items = Todo.objects.all()
    return render(request, 'index.html')

def scrape(request):
    # todo_items = Todo.objects.all()
    return render(request, 'scrape.html')


def search(request):
    if request.method == 'GET':
        if request.GET.get('model'):
            search = request.GET.get('model')
            print("search:"+ search)
            if request.GET.get('darazcheck') and request.GET.get('sastodealcheck'):
                todo_items = Daraz.objects.filter(title__contains=search).order_by('price')
                sasto_item = SastoDeal.objects.filter(title__contains=search).order_by('price')

            elif request.GET.get('darazcheck'):
                todo_items = Daraz.objects.filter(title__contains=search)
                sasto_item= None
            elif request.GET.get('sastodealcheck'):
                sasto_item = SastoDeal.objects.filter(title__contains=search)
                todo_items= None
        else:
            search = request.GET.get('model')
            print("search:" + search)
            # search = request.GET.get('model')
            # todo_items = Daraz.objects.filter(title__contains=search)
            # sasto_item = SastoDeal.objects.filter(title__contains=search)
            todo_items=None
            sasto_item=None

        return render(request, 'search.html', {'todo_items': todo_items, 'sasto_item': sasto_item})

def sastodeal_item(request):
    SastoDeal.objects.all().delete()
    # driver = webdriver.Chrome('E:\chromedriver_win32/chromedriver')
    driver = webdriver.Chrome('D:\office/chromedriver')

    driver.get(
        f'https://www.sastodeal.com/electronic/laptops/dell.html'
    )

    productlink = []
    page = driver.page_source
    page = driver.execute_script("return document.documentElement.outerHTML")

    pg_soup = soup(page, "lxml")

    contain = pg_soup.findAll("div", {"class": "actions-primary"})

    for items in contain:
        for link in items.findAll('a', href=True):
            productlink.append(link['href'])
        print(productlink)

    for links in productlink:
        driver.get(links)
        page = driver.page_source
        pg_soup = soup(page, "lxml")

        brand = pg_soup.find('span', attrs={'class': 'col data'}).text
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


def add_item(request):
    Daraz.objects.all().delete()
    # driver = webdriver.Chrome('E:\chromedriver_win32/chromedriver')
    driver = webdriver.Chrome('D:\office/chromedriver')
    # baseurl = "https://www.daraz.com.np/"
    # def getlaps(page):
    for x in range(1, 3):
        driver.get(
            f'https://www.daraz.com.np/laptops/dell/?page={x}')

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
        print(productlink)

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
            Daraz.objects.create(brand =  brand,
                        title= title,
                        price= price,
                        category= category,
                        original= orginal,
                        discount= discount,)
    return redirect("scrape")


# def delete_item(request, item_id):
#     Todo.objects.get(id=item_id).delete()
#     return redirect("index")