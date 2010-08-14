#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Bookee(object):
	def __init__(self, name, isbn, author, publisher, link, price):
		self.name = name
		self.isbn = isbn
		self.author = author
		self.publisher = publisher
		self.link = link
		self.price = price

	def __repr__(self):
		return u"<Book('%s', '%s', '%s', '%s', '%f')>" % (self.name, self.author, self.publisher, self.link, self.price)


class Book(Bookee):
	def to_bookee(self):
		bokee = Bookee(self.name, self.isbn, self.author, self.publisher, self.link, self.price)
		bokee.isbn = str(bokee.isbn)
		return bokee

