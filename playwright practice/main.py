"""
Scraping steps:
    1. Open a page
    2. Locate the repeating items (products, posts, rows)
    3. Extract fields from each item
    4. Move on (next page, scroll, next URL)
    5. Save what you collected


Before writing code, you need to know what to point at. Two ways:

    Open the site in Chrome, right-click a book, choose Inspect.
    Find the element that wraps one whole book. Here it's <article class="product_pod">.
    Look inside it for the pieces you want: the title, price, and so on
"""

from playwright.sync_api import sync_playwright
from pathlib import Path

#opening section opens the browser to go to site
with sync_playwright() as p:
    #headless=False: opens visual page of chrome
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    #https://books.toscrape.com site to practice scraping
    #tells browser what page to go to and waits for page to load
    page.goto("https://books.toscrape.com")

    #finds all <article class="product_pod">
    books = page.locator("article.product_pod")

    #prints number of books found from above line
    print(books.count())


    results = []
    for card in books.all():
        title = card.locator("h3 a").get_attribute("title")

        price = card.locator("p.price_color").inner_text()
        price = float(price.replace('£', ''))

        link = card.locator("h3 a").get_attribute("href")
        link = "https://books.toscrape.com/" + link

        star_rating = card.locator("p.star-rating").get_attribute("class")
        star_rating = star_rating.split()[-1]

        results.append({'title': title, 'price': price, 'link': link, 'rating': star_rating})

    #closes the browser when done
    browser.close()

with open ('results.txt', 'w') as file:
    for n in results:
        file.write(f'{n}\n')