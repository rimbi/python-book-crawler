# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.xlib.pydispatch import dispatcher
from scrapy.core import signals
from storm.locals import *
from string import replace

class Book(object):
	__storm_table__ = "books"
	id = Int(primary=True)
	isbn		= Unicode()
	name		= Unicode()
	author		= Unicode()
	publisher   = Unicode()
	link		= Unicode()
	price	   	= Float()
	store	   	= Int()

class DbExportPipeline(object):

	def __init__(self):
		dispatcher.connect(self.spider_opened, signals.spider_opened)
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		self.store = None

	def spider_opened(self, spider):
		db = create_database("sqlite:///books.db")
		self.store = Store(db)
			
	def spider_closed(self, spider):
		self.store.flush()
		self.store.commit()
		self.store.close()

	
	def process_item(self, spider, item):
		book = Book()
		book.isbn = item['isbn'].strip().replace("-", "")
		if len(book.isbn) == 13:
			book.isbn = book.isbn[-10:]
		book.name	   	= unicode(item['name'].strip())
		book.author		= unicode(item['author'].strip())
		book.publisher  = unicode(item['publisher'].strip())
		book.link	   	= unicode(item['link'].strip())
		book.price	  	= float(replace(item['price'], ',', '.'))
		book.store	  	= item['store']
		self.store.add(book)
		return item

