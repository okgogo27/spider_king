import scrapy
import json
from bs4 import BeautifulSoup
from spider_king.items import SpiderKingItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    url_forward = 'http://www.toutiao.com/a'

    def start_requests(self):
        urls = [
            'http://www.toutiao.com/search_content/?offset=3&format=json&keyword=%E9%94%80%E5%94%AE&autoload=true&count=20&cur_tab=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body,"html.parser")
        json_str = json.loads(soup.text)
        for item in json_str['data']:
            for key in item.keys():
                if key == 'source_url':
                    url = self.url_forward + item[key].split('/')[-2]
                    yield scrapy.Request(url=url, callback=self.parse_article)

    def parse_article(self,response):
        soup = BeautifulSoup(response.body,'lxml')
        item = SpiderKingItem()
        item['title'] = soup.find('h1',attrs={'class':'article-title'}).text
        item['text'] = soup.find('div',attrs={'class':'article-content'})
        item['page_url'] = response.url

        imgs = soup.find_all('img')
        img_list = []
        for img in imgs:
            if 's3.pstatp.com' in img.get('src'):
                continue
            img_list.append(img.get('src'))
        item['img_url'] = img_list

        keywords = soup.find_all('a',attrs={'class':'label-link'})
        keyword_f = ''
        for keyword in keywords:
            keyword_f=keyword.text+','
        item['keyword'] = keyword_f[:-1]

        yield item

