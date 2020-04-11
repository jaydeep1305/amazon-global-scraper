import scraper
import database
from loguru import logger
from database import Database
from scraper import Scraper

DB_USER = "root"
DB_PASS = "nopassword1305"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_DATABASE = "foldingbikeguides"
DOMAIN_URL = "https://foldingbikeguides.com"
SITEMAP_URL = "https://foldingbikeguides.com/post-sitemap.xml"

scraper_obj = Scraper(SITEMAP_URL)

database_obj = Database(DB_HOST,DB_PORT,DB_USER,DB_PASS)
database_obj.create_database(DB_DATABASE)
database_obj.create_connection()
database_obj.create_table()
database_obj.create_connection()

URLS = scraper_obj.get_sitemap()
database_obj.save_urls(URLS)

while True:
    cat_url = database_obj.get_cat_url()
    if cat_url is not None:
        cat_url = cat_url[0]
        category,asin = scraper_obj.parse(cat_url,DOMAIN_URL)
        if category is not None:
            if asin is not None:
                asin = set(asin)
                database_obj.save_amazon(category,asin,cat_url,scraper_obj)