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


engine = create_engine('sqlite:///%s' % sys.argv[1], echo=True)
metadata = MetaData()

books_table = Table('books', metadata,
			Column('id', Integer, primary_key=True),
			Column('isbn', Integer),
			Column('name', Unicode),
			Column('author', Unicode),
			Column('publisher', Unicode),
			Column('link', Unicode),
			Column('price', Float),
			Column('store', Integer))

metadata.create_all(engine)

