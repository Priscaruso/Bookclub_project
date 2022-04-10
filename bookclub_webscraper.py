# python script that collects data from book club platform

# it imports the libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.firefox.options import Options

# defines an option to not show the browser navigation
options = Options()
options.add_argument('--headless')

# it creates the browser object and navigates to the url page mentioned
browser = webdriver.Firefox(options=options)
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

    # it searches for the desired tag and class of the book
    book_container = site.find_all('div', class_='image_container')

    # the url base
    base_url = 'https://books.toscrape.com/catalogue/'

    # it gets the book's links and stores them in the book_links list
    for link in book_container:
        book_links.append(base_url + link.a['href'])

# it opens the data_bookclub.csv file, adding new data into it using the UTF-8 encoding
file = open('data_bookclub.csv', 'a', encoding='UTF-8')

# it gets book's url stored in the book_links list and navigates to its page. Then it collects the desired book data
for url in book_links:
    # it navigates to the book's page and waits 2 seconds until it's fully loaded
    browser.get(url)

    # it takes a print of the HTML content of the page, stores in the variable book_content and downloads the
    # html content of the page into the beautifulsoup object book_page
    book_content = browser.page_source
    book_page = BeautifulSoup(book_content, 'html.parser')

    # it gets the html parse tree where is the main information from the book
    book_info = book_page.find('div', class_='col-sm-6 product_main')

    # it gets the book name
    book_name = book_info.find('h1').get_text()

    # it gets the book category name
    book_category = book_page.find('ul', class_='breadcrumb').get_text()
    book_category = list(book_category.strip().split('\n'))
    book_category = book_category[6]

    # it gets the book number of stars
    book_stars = book_info.find('p', class_='star-rating').get('class')
    book_stars = book_stars[1]

    # it gets the book price
    book_price = book_info.find('p', class_='price_color').get_text()

    # it gets the book availability
    book_availability = book_info.find('p', class_='instock availability').get_text().strip()
    book_availability = book_availability[:8]

    # it concatenates all the desired data separating each of them with ; and writes it into the data_bookclub.csv file
    data = book_name + ';' + book_category + ';' + book_stars + ';' + book_price + ';' + book_availability + '\n'
    file.write(data)
