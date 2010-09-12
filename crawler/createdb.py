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


engine = create_engine('mysql://root:123456@localhost/bookcrawler', echo=True)
metadata = MetaData()

books_table = Table('books', metadata,
			Column('id', Integer, primary_key=True),
			Column('isbn', Unicode(255)),
			Column('name', Unicode(255)),
			Column('author', Unicode(255)),
			Column('publisher', Unicode(255)),
			Column('link', Unicode(255)),
			Column('price', Float(precision=2)),
			Column('store', Integer)
			)

metadata.create_all(engine)
