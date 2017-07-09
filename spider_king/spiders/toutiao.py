import scrapy
import json
import traceback
from bs4 import BeautifulSoup
from spider_king.items import SpiderKingItem
from spider_king.sqliteDB import sqliteDB
from spider_king.utils import logger


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    url_forward = 'http://www.toutiao.com/a'

    def start_requests(self):
        urls = [
            'http://www.toutiao.com/search_content/?offset=20&format=json&keyword=%E9%94%80%E5%94%AE&autoload=true&count=20&cur_tab=1',
            'http://www.toutiao.com/search_content/?offset=40&format=json&keyword=%E9%94%80%E5%94%AE&autoload=true&count=20&cur_tab=1',
            'http://www.toutiao.com/search_content/?offset=60&format=json&keyword=%E9%94%80%E5%94%AE&autoload=true&count=20&cur_tab=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            soup = BeautifulSoup(response.body,"html.parser")
            json_str = json.loads(soup.text)
            db = sqliteDB()
            for item in json_str['data']:
                for key in item.keys():
                    if key == 'source_url':
                        url = self.url_forward + item[key].split('/')[-2]
                        if db.query(url):
                            continue
                        yield scrapy.Request(url=url, callback=self.parse_article)
            db.close()
        except:
            logger.error(traceback.format_exc())

    def parse_article(self,response):
        try:
            soup = BeautifulSoup(response.body,'lxml')
            item = SpiderKingItem()
            title = soup.find('h1', attrs={'class': 'article-title'})
            item['title'] = title.text if title else ''
            item['text'] = soup.find('div',attrs={'class':'article-content'})
            item['page_url'] = response.url

            imgs = soup.find_all('img')
            img_list = []
            for img in imgs:
                if 's3.pstatp.com' in img.get('src') or ('http' not in img.get('src')):
                    continue
                img_list.append(img.get('src'))
            item['img_url'] = img_list

            keywords = soup.find_all('a',attrs={'class':'label-link'})
            keyword_f = ''
            for keyword in keywords:
                keyword_f=keyword.text+','
            item['keyword'] = keyword_f[:-1]

            yield item
        except:
            logger.error(traceback.format_exc())

