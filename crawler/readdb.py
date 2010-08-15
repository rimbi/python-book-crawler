#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import sys
import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float, Unicode, MetaData, ForeignKey, or_
from sqlalchemy.orm import mapper, sessionmaker
from optparse import OptionParser

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


parser=OptionParser()
parser.add_option("-d", "--database", dest="database_name", help="select database file name", metavar="DATABASE")
parser.add_option("-c", "--column", dest="column_name", help="select column name", metavar="COLUMN")
parser.add_option("-q", "--query", dest="query_string", help="set query string", metavar="QUERY")
(options, args) = parser.parse_args()

engine = create_engine('sqlite:///%s' % options.database_name, echo=True)
metadata = MetaData()

books_table = Table('books', metadata,
			Column('id', Integer, primary_key=True),
			Column('isbn', Unicode),
			Column('name', Unicode),
			Column('author', Unicode),
			Column('publisher', Unicode),
			Column('link', Unicode),
			Column('price', Float),
			Column('store', Integer))

mapper(Book, books_table)
Session = sessionmaker(bind=engine)
session = Session()

query=unicode(options.query_string, encoding="utf_8")
expressions = { "name"      : Book.name.like(u"%" + query + u"%"),
                "author"    : Book.author.like(u"%" + query + u"%"),
                "publisher" : Book.publisher.like(u"%" + query + u"%"),
                "isbn"      : Book.isbn == query,
              }

for book in session.query(Book).filter(expressions[options.column_name]).order_by(Book.price):
	print "---------------------"
	print "%s\n %s\n %s\n %s\n %s\n %f\n %d\n" % (book.name, book.author, book.publisher, book.link, book.isbn, book.price, book.store)
