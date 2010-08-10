# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader.processor import Join, TakeFirst

class JobItem(Item):
    # define the fields for your item here like:
    title = Field(
            default = u'http://www.yenibiris.com',
    )
    link = Field(
            default = u'Başlık',
    )
    desc = Field(
            default = u'İş tanımı',
            output_processor=Join(),
    )

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
    )

