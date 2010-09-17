#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float, Unicode, MetaData
from argparse import ArgumentParser

parser = ArgumentParser(description='Allows to create initial books table in mysql database')
parser.add_argument('-u', '--username', nargs=1, default=['root'], help='Username of the relevant database')
parser.add_argument('-p', '--password', nargs=1, default=[''], help='Password for given or default username of the relevant database')
parser.add_argument('--host', nargs=1, default=['localhost'], help='Host address of the database')
parser.add_argument('-d', '--database', nargs=1, default=['bookcrawler'], help='Database name')
options = parser.parse_args()

db_dialect = "mysql://" + options.username[0] + ":" + options.password[0] + "@" + options.host[0] + "/" + options.database[0]
engine = create_engine(db_dialect, echo=True)
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
