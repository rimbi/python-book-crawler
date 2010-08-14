#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Bookee(object):
	def __init__(self, name, isbn, author, publisher, link, pricei, store):
		self.name = name
		self.isbn = isbn
		self.author = author
		self.publisher = publisher
		self.link = link
		self.price = price
		self.store = store

	def __repr__(self):
		return u"<Book('%s', '%s', '%s', '%s', '%f' '%d')>" % (self.name, self.author, self.publisher, self.link, self.price, self.store)


class Book(Bookee):
	def to_bookee(self):
		bokee = Bookee(self.name, self.isbn, self.author, self.publisher, self.link, self.price, self.store)
		bokee.isbn = str(bokee.isbn)
		return bokee

