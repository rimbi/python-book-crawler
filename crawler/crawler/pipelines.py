# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.xlib.pydispatch import dispatcher
from scrapy.core import signals
from string import replace
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float, Unicode, MetaData, ForeignKey, or_, DECIMAL
from sqlalchemy.orm import mapper, sessionmaker

class Book(object):
	def __init__(self, name, isbn, author, publisher, link, price, store):
		self.name = name
		self.isbn = isbn
		self.author = author
		self.publisher = publisher
		self.link = link
		self.price = price
		self.store = store

	def __repr__(self):
		return u"<Book('%s', '%s', '%s', '%s', '%s', '%f' '%d')>" % (self.name, self.isbn, self.author, self.publisher, self.link, self.price, self.store)

metadata = MetaData()

books_table = Table('books', metadata,
			Column('id', Integer, primary_key=True),
			Column('isbn', Unicode(255)),
			Column('name', Unicode(255)),
			Column('author', Unicode(255)),
			Column('publisher', Unicode(255)),
			Column('link', Unicode(255)),
			Column('price', Float(precision=2)),
			Column('store', Integer))

mapper(Book, books_table)

class DbExportPipeline(object):
	i = 0
	def __init__(self):
		dispatcher.connect(self.spider_opened, signals.spider_opened)
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		self.session = None

	def spider_opened(self, spider):
		self.session = sessionmaker(bind=create_engine('mysql://root:123456@localhost/bookcrawler', echo=True))()
		DbExportPipeline.i += 1

	def spider_closed(self, spider):
		DbExportPipeline.i -= 1
		if DbExportPipeline.i == 0:
			self.session.close()

	def process_item(self, spider, item):
		book_isbn = item['isbn'].strip().replace("-", "")
		if len(book_isbn) == 13:
			book_isbn = book_isbn[-10:]
		book_name	   	= unicode(item['name'].strip())
		book_author		= unicode(item['author'].strip())
		book_publisher  	= unicode(item['publisher'].strip())
		book_link	   	= unicode(item['link'].strip())
		book_price	  	= float(replace(item['price'], ',', '.'))
		book_store	  	= item['store']
		book = Book(book_name, book_isbn, book_author, book_publisher, book_link, book_price, book_store)
		self.session.add(book)
		self.session.flush()
		self.session.commit()
		return item

