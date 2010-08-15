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

from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from book import Book, Bookee


parser=OptionParser()
parser.add_option("-d", "--database", dest="database_name", help="select database file name", metavar="DATABASE")
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

def query_books(query_string, column_name):
	query=unicode(query_string, encoding="utf_8")
	expressions = { "name"	 	: Book.name.like(u"%" + query + u"%"),
					"author"	: Book.author.like(u"%" + query + u"%"),
					"publisher" : Book.publisher.like(u"%" + query + u"%"),
                    "isbn"      : Book.isbn == query,
	}
	
	for book in session.query(Book).filter(expressions[column_name]).order_by(Book.price):
		print "---------------------"
		print "%s\n %s\n %s\n %s\n %s\n %f\n %d\n" % (book.name, book.author, book.publisher, book.link, book.isbn, book.price, book.store)
		
	return [book.to_bookee() for book in session.query(Book).filter(expressions[column_name]).order_by(Book.price)]

xml_rpc_server = SimpleXMLRPCServer(("localhost", 5555), allow_none=True)
xml_rpc_server.register_introspection_functions()
xml_rpc_server.register_function(query_books);

xml_rpc_server.serve_forever()

