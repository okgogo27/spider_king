# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import time
import os

class SpiderKingPipeline(object):
    def process_item(self, item, spider):
        return item

class ImageDownLoadPipeline(ImagesPipeline):

    year = time.strftime('%Y%m', time.localtime(time.time()))
    day = time.strftime('%d', time.localtime(time.time()))

    window_path = 'D:\\test\\'

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
        path = self.window_path + self.year + '\\' + self.day
        if not os.path.exists(path):
            os.makedirs(path)
        name = path+'\\' + request.url.split('/')[-1]+'.jpg'
        return name
