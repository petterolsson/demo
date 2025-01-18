from scrapy import Spider

# Define a spider class for scraping the Books to Scrape website
class BooksToScrapeComSpider(Spider):
    # Name of the spider
    name = "books_toscrape_com"
    # Initial URL to start scraping from
    start_urls = [
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    ]
    metadata = {
    "title": "My Demo Template",
    "description": "This is a Demo template.",
    "template": True,
    }

    # Method to parse the response from the initial URL
    def parse(self, response):
        # Select the link to the next page and follow it
        next_page_links = response.css(".next a")
        yield from response.follow_all(next_page_links)
        # Select all book links on the current page and follow them
        book_links = response.css("article a")
        yield from response.follow_all(book_links, callback=self.parse_book)

    # Method to parse the response from each book link
    def parse_book(self, response):
        # Extract and yield the book's name, price, and URL
        yield {
            "name": response.css("h1::text").get(),
            "price": response.css(".price_color::text").re_first("£(.*)"),
            "url": response.url,
        }