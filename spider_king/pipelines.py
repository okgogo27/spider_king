# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from spider_king.utils import confLoad
from spider_king.sqliteDB import sqliteDB
from spider_king.utils import logger
import traceback
import time
import os
import csv

class ToutiaoPipeline(object):

    year = time.strftime('%Y%m', time.localtime(time.time()))
    day = time.strftime('%d', time.localtime(time.time()))

    fieldnames = ['title', 'text', 'keyword', 'page_url']

    def process_item(self, item, spider):
        db = sqliteDB()
        try:
            path = confLoad.get('path','root_path')+ 'data\\' + self.year + self.day+'toutiao.csv'
            if not os.path.exists(path):
                with open(path,'w',newline='') as csvfile:
                    writer = csv.DictWriter(csvfile,fieldnames=self.fieldnames)
                    writer.writeheader()
            with open(path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([item['title'], item['text'], item['keyword'], item['page_url']])
            db.insert(item['page_url'])
        except:
            db.insert(item['page_url'])
            logger.error(traceback.format_exc())
        db.close()
        return item

class ImageDownLoadPipeline(ImagesPipeline):

    year = time.strftime('%Y%m', time.localtime(time.time()))
    day = time.strftime('%d', time.localtime(time.time()))

    def get_media_requests(self, item, info):
        for image_url in item['img_url']:
            yield scrapy.Request(image_url)

    # def item_completed(self, results, item, info):
    #     image_paths = [x['path'] for ok, x in results if ok]
    #     if not image_paths:
    #         raise DropItem("Item contains no images")
    #     item['image_paths'] = image_paths
    #     return item

    def file_path(self, request, response=None, info=None):
        path = confLoad.get('path','root_path')+ 'img\\' + self.year + '\\' + self.day
        if not os.path.exists(path):
            os.makedirs(path)
        name = path+'\\' + request.url.split('/')[-1]+'.jpg'
        return name
