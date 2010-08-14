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

import xmlrpclib
from book import Bookee


parser=OptionParser()
parser.add_option("-c", "--column", dest="column_name", help="select column name", metavar="COLUMN")
parser.add_option("-q", "--query", dest="query_string", help="set query string", metavar="QUERY")
(options, args) = parser.parse_args()

query=unicode(options.query_string, encoding="utf_8")

book_service = xmlrpclib.ServerProxy('http://localhost:5555')
books = book_service.query_books(options.query_string, options.column_name)

for entry in books:
	book = Bookee(entry["name"], entry["isbn"], entry["author"], entry["publisher"], entry["link"], entry["price"])
	print "---------------------"
	print "%s\n %s\n %s\n %s\n %s\n %f\n" % (book.name, book.author, book.publisher, book.link, book.isbn, book.price)
