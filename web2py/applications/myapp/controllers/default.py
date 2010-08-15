# -*- coding: utf-8 -*- 

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  

def index():
    books = db(db.books.name.like(u'%bilgi%')).select(orderby=db.books.name)
    return dict(books=books)

def query():
    query_string = unicode(request.vars.query_string)
    column_name = request.vars.column_name
    like_string = u'%' + query_string + u'%'
    expressions = {
        "name"      : db.books.name.like(like_string),
        "author"    : db.books.author.like(like_string),
        "publisher" : db.books.publisher.like(like_string),
        "isbn"      :  db.books.isbn == query_string,
    }

    books = db(expressions[request.vars.column_name]).select(orderby=db.books.price)
    return dict(books=books)
