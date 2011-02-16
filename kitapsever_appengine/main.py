#!/usr/bin/env python
#

import os
import urllib

from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class Book(db.Model):
    isbn = db.StringProperty()
    link = db.StringProperty()
    price = db.FloatProperty()
    store = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
        self.response.out.write('<html><body>')
        self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit" 
            name="submit" value="Submit"> </form></body></html>""")

class AllBooksQueryHandler(webapp.RequestHandler):
    def get(self):
		books = Book.gql("ORDER BY price ")

		template_values = {
			'books': books,
		}

		path = os.path.join(os.path.dirname(__file__), 'results.xml')
		self.response.out.write(template.render(path, template_values))

class FirstBookByISBNQueryHandler(webapp.RequestHandler):
    def get(self):
		isbn  = self.request.get('isbn')

		books = Book.gql("WHERE isbn = :1 "
						 "ORDER BY price "
						 "LIMIT 1", isbn)

		template_values = {
			'books': books,
		}

		path = os.path.join(os.path.dirname(__file__), 'results.xml')
		self.response.out.write(template.render(path, template_values))

class AllBooksByISBNQueryHandler(webapp.RequestHandler):
    def get(self):
		isbn  = self.request.get('isbn')

		books = Book.gql("WHERE isbn = :1 "
						 "ORDER BY price "
						 , isbn)

		template_values = {
			'books': books,
		}

		path = os.path.join(os.path.dirname(__file__), 'results.html')
		self.response.out.write(template.render(path, template_values))

class BookQueryHandler(webapp.RequestHandler):
    def get(self):
		isbn  = self.request.get('isbn')
		link  = self.request.get('link')
		price = self.request.get('price')
		store = self.request.get('store')
		q = Book.gql("WHERE isbn = :1 AND store = :2", isbn, int(store))
		book = q.get()
		if book is None:
			book = Book()
		book.isbn = isbn
		book.link = link
		book.price = float(price)
		book.store = int(store)
		book.put()	

		books = Book.gql("WHERE isbn = :1 "
						 "ORDER BY price "
						 "LIMIT 1", isbn)

		template_values = {
			'books': books,
		}

		path = os.path.join(os.path.dirname(__file__), 'results.xml')
		self.response.out.write(template.render(path, template_values))

class DatabaseCleanHandler(webapp.RequestHandler):
	def get(self):
		books = Book.gql("LIMIT 5000")
		db.delete(books)
		self.response.out.write("Number of remaining items is %d" % db.GqlQuery("SELECT * FROM Book").count())

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
		blob_info = upload_files[0]
		blob_reader = blobstore.BlobReader(blob_info.key())
		for line in blob_reader:
			book = Book()
			items = line[:len(line)-1].split(";")
			book.isbn = items[0]
			book.link = items[1]
			book.price = float(items[2])
			book.store = int(items[3])
			print book.link
			book.put()
		blob_info.delete()
		self.redirect('/serve')

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self):
		isbn  = self.request.get('isbn')
		link  = self.request.get('link')
		price = self.request.get('price')
		store = self.request.get('store')
		books = Book.gql("WHERE isbn = :1 AND store = :2 "
						 "ORDER BY price "
						 "LIMIT 1", isbn, int(store))

		template_values = {
			'books': books,
		}

		path = os.path.join(os.path.dirname(__file__), 'results.xml')
		self.response.out.write(template.render(path, template_values))

def main():
	application = webapp.WSGIApplication(
		[('/', MainHandler),
		 ('/upload', UploadHandler),
		 ('/serve', ServeHandler),
		 ('/clean', DatabaseCleanHandler),
		 ('/book', BookQueryHandler),
		 ('/bookbyisbn', FirstBookByISBNQueryHandler),
		 ('/booksbyisbn', AllBooksByISBNQueryHandler),
		 ('/allbooks', AllBooksQueryHandler),
		], debug=True)
	run_wsgi_app(application)

if __name__ == '__main__':
	main()
