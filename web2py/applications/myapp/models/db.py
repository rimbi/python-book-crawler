# -*- coding: utf-8 -*- 
from database_config import DatabaseConfig

db = DAL(DatabaseConfig().get_dialect())

db.define_table('books',
   Field('name'),
   Field('author'),
   Field('isbn'),
   Field('publisher'),
   Field('price', 'double'),
   Field('link'),
   Field('store', 'integer'),
   migrate=False)
