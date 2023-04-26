# python script that collects data from book club platform

# it imports the libraries
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd


def get_book_links(browser):
    """ Function that navigates to the url page mentioned and get book links
    :param browser: obj the browser object
    :return: list - a list containing all book's links

    It navigates to the book platform page, iterates over all the website pages collecting all book's links and storing
    them inside a list.
    """

    browser.get('https://books.toscrape.com/')

    # it waits 2s until the page is fully loaded
    sleep(2)

    # the list to store each book link
    book_links = []

    # it iterates over all the website pages and collects all book's links
    for i in range(1, 51):

        # the browser navigates to the desired page
        url = f'https://books.toscrape.com/catalogue/page-{i}.html'
        browser.get(url)

        # it takes a print of the HTML content of the page and stores in the variable page_content
        page_content = browser.page_source

        # site object gets (downloads) the html content from page_content
        site = BeautifulSoup(page_content, 'html.parser')

        # it searches for the desired tag e class of the book
        book_container = site.find_all('div', class_='image_container')

        # the url base
        base_url = 'https://books.toscrape.com/catalogue/'

        # it gets the book's links and stores them in the book_links list
        for link in book_container:
            book_links.append(base_url + link.a['href'])
        
    return book_links


def get_book_data(browser, book_links):
    """Function that gets book's data

    :param browser: obj the browser object
    :param book_links: list contains all books' links
    :return: list - contains all the desired book's data

    It navigates to the book's page and collects book's name, category, number of stars, price and availability, storing all 
    data inside of a list.
    """

    # list to store all books' data
    complete_book_data = []

    # it gets book's url stored in the book_links list and navigates to its page. Then it collects the desired book data
    for url in book_links:

        book_data = []
        # navigates to the book's page and waits 2 seconds until it's fully loaded
        browser.get(url)
        sleep(2)

        # it takes a print of the HTML content of the page, stores in the variable book_content and downloads html content
        # of the page into the beautifulsoup object book_page
        book_content = browser.page_source
        book_page = BeautifulSoup(book_content, 'html.parser')

        # it gets the html parse tree where is the main information from the book
        book_info = book_page.find('div', class_='col-sm-6 product_main')

        # it gets the book name
        book_name = book_info.find('h1').get_text()
        book_data.append(book_name)

        # it gets the book category name
        book_category = book_page.find('ul', class_='breadcrumb').get_text()
        book_category = list(book_category.strip().split('\n'))
        book_category = book_category[6]
        book_data.append(book_category)

        # it gets the book number of stars
        book_stars = book_info.find('p', class_='star-rating').get('class')
        book_stars = book_stars[1]
        book_data.append(book_stars)

        # it gets the book price
        book_price = book_info.find('p', class_='price_color').get_text()
        book_price = book_price[1:]
        book_data.append(book_price)

        # it gets the book availability
        book_availability = book_info.find('p', class_='instock availability').get_text().strip()
        book_availability = book_availability[:8]
        book_data.append(book_availability)

        # it stores all book data inside the complete_book_data list
        complete_book_data.append(book_data)

    browser.quit()
    return complete_book_data


