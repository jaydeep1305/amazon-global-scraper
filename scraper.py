import requests
import re
import sys
from bs4 import BeautifulSoup
from loguru import logger
from lxml import html


class Scraper:
    def __init__(self,SITEMAP):
        self.SITEMAP = SITEMAP

    def get_sitemap(self):
        xml_data = []
        r = requests.get(self.SITEMAP)
        xml = r.text
        soup = BeautifulSoup(xml,'lxml')
        sitemapTags = soup.find_all("url")
        for sitemap in sitemapTags:
            xml_data.append(sitemap.findNext("loc").text)
        
        return xml_data

    def parse(self,URL,DOMAIN_URL):
        if DOMAIN_URL in URL : 
            logger.info("Parsing - " + URL)
            page = requests.get(URL)
            tree = html.fromstring(page.content)
            data = tree.xpath('//a[contains(@href,"https://www.amazon.com/dp/")]')
            asin = []
            category = URL.replace(DOMAIN_URL,"")
            category = re.sub('[^0-9a-zA-Z-]+','',category)
            for _data in data:
                _data = _data.xpath("@href")
                _data = re.search(r'dp/(.*?)\?',_data[0])
                asin.append(_data.group(1))
            return category,asin
        if "https://amazon.com/dp/" in URL:
            # logger.info("Parsing - " + URL)
            try:
                headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
                page = requests.get("http://khannainternational.com/middle/?url="+URL, headers=headers)
                if page.status_code == 200:
                    tree = html.fromstring(page.content)
                    data = tree.xpath('//*[@id="productTitle"]/text()')
                    if data:
                        data = data[0]
                        product_name = data.replace('\n', '')
                        product_name = product_name.replace('"', '\\\"')
                        product_name = product_name.replace("'", "\\\'")
                        product_name = product_name.strip()
                    else :
                        product_name = "--error--"
                else:
                    product_name = "--error-inner--"
            except Exception as e:
                product_name = "--manual--"

            return product_name
        