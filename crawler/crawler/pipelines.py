# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.xlib.pydispatch import dispatcher
from scrapy.core import signals
from string import replace
from crawler.settings import BOOK_SERVICE_ADDRESS
import urllib2

ITEM_SEPERATOR = ";"

class FileExportPipeline(object):
	def __init__(self):
		dispatcher.connect(self.spider_opened, signals.spider_opened)
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		self.out_file = None

	def spider_opened(self, spider):
		self.out_file = open(spider.domain_name + ".txt", "w")

	def spider_closed(self, spider):
		self.out_file.close()

	def process_item(self, spider, item):
		isbn = item['isbn'].strip().replace("-", "")
		if len(isbn) == 13:
			isbn = isbn[-10:]
		link  = item['link'].strip()
		price = replace(item['price'], ',', '.')
		store = str(item['store'])
		line  = isbn + ITEM_SEPERATOR
		line  = line + link + ITEM_SEPERATOR
		line  = line + price + ITEM_SEPERATOR
		line  = line + store + "\n"
		self.out_file.write(line)
		service_link = BOOK_SERVICE_ADDRESS + '?isbn=' + isbn + '&price=' + price + '&store=' + store + '&link=' + link
		urllib2.urlopen(service_link)
		return item

