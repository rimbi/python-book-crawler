# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader.processor import Join, TakeFirst, Compose

class BookItem(Item):
    # define the fields for your item here like:
    isbn = Field(
            default = u'0',
            output_processor = TakeFirst(),
    )
    name = Field(
            default = u'Kitap',
            output_processor = Join(),
    )
    author = Field(
            default = u'Yazar',
            output_processor = Join(),
    )
    publisher = Field(
            default = u'Yayınevi',
            output_processor = Join(),
    )
    link = Field(
            default = u'Bağlantı',
            output_processor = TakeFirst(),
    )
    price = Field(
            default = u'0 TL',
            output_processor = TakeFirst(),
            input_processor = Compose(lambda v: v[-1:]),
    )
    store = Field(
            default = 0,
            output_processor = TakeFirst(),
    )

