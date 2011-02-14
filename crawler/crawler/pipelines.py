# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.xlib.pydispatch import dispatcher
from scrapy.core import signals
from string import replace

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
		book_isbn = item['isbn'].strip().replace("-", "")
		if len(book_isbn) == 13:
			book_isbn = book_isbn[-10:]
		line = book_isbn + ITEM_SEPERATOR
		line = line + item['link'].strip() + ITEM_SEPERATOR
		line = line + replace(item['price'], ',', '.') + ITEM_SEPERATOR
		line = line + str(item['store']) + "\n"
		self.out_file.write(line)
		return item

