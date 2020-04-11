import sys
import mysql.connector 
from loguru import logger

class Database:
    def __init__(self,DB_HOST,DB_PORT,DB_USER,DB_PASS):
        self.DB_HOST = DB_HOST
        self.DB_PORT = DB_PORT
        self.DB_USER = DB_USER
        self.DB_PASS = DB_PASS

        self.connection = mysql.connector.connect(host=self.DB_HOST,
            port=self.DB_PORT,
            user=self.DB_USER,
            password=self.DB_PASS)
        self.cursor = self.connection.cursor(buffered=True)

    def create_database(self,DB_DATABASE):
        self.DB_DATABASE = DB_DATABASE
        create_db = 'CREATE DATABASE IF NOT EXISTS '+str(self.DB_DATABASE)+';'
        self.cursor.execute(create_db)
        self.connection.commit()
        logger.debug("Database created.")
        
    def create_connection(self):
        self.connection = mysql.connector.connect(host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_DATABASE,
            user=self.DB_USER,
            password=self.DB_PASS)
        self.cursor = self.connection.cursor(buffered=True)
        logger.debug("Connection created successfully.")

    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS `urls` (`urls_id` int(11) NOT NULL AUTO_INCREMENT,`url` varchar(700) NOT NULL,`status` int(11) NOT NULL DEFAULT '0', PRIMARY KEY (`urls_id`), UNIQUE KEY `url` (`url`));")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS `amazon` (`id` int(11) NOT NULL AUTO_INCREMENT, `category` varchar(500) NOT NULL,  `asin` varchar(500) NOT NULL,  `product_name` varchar(5000) DEFAULT NULL,  `status` int(11) NOT NULL DEFAULT '0', PRIMARY KEY (`id`), UNIQUE KEY `asin` (`asin`));")
        self.connection.commit()
    
    def save_urls(self,URLS):
        for url in URLS:
            insert = "INSERT IGNORE INTO urls (url) VALUES('"+url+"');"
            self.cursor.execute(insert)
            if self.cursor.lastrowid != 0:
                logger.debug("urls saved - " + url)
        self.connection.commit()
    
    def get_cat_url(self):
        select = "SELECT url from urls where status = 0 AND url <> 'https://toptenz.co';"
        self.cursor.execute(select)
        url = self.cursor.fetchone()
        return url
    
    def save_amazon(self,category,asin,cat_url,scraper_obj):
        bulk_asin = asin
        for asin in bulk_asin:            
            product_name = scraper_obj.parse("https://amazon.com/dp/"+asin,"https://www.amazon.com/")
            if product_name is not None:
                logger.info(category + " - " + asin + " - " + product_name)
                insert = "INSERT IGNORE INTO amazon (category,asin,product_name,status) VALUES('"+category+"','"+asin+"','"+product_name+"',1)"
                self.cursor.execute(insert)
            else :
                logger.error("--- AMAZON ERROR ---")
                sys.exit()

        update = "UPDATE urls set status = 1 where url = '" + cat_url + "'"
        self.cursor.execute(update)
        self.connection.commit()
