# -*- coding: utf-8 -*- 
db = DAL("sqlite://books.db")

db.define_table('books',
   Field('name'),
   Field('author'),
   Field('isbn', 'integer'),
   Field('publisher'),
   Field('price', 'double'),
   Field('link'),
   migrate=False)
