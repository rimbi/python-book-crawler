# -*- coding: utf-8 -*-

import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawler.items import BookItem
from scrapy.contrib.loader import XPathItemLoader

class IlknoktaSpider(CrawlSpider):
    domain_name = 'ilknokta.com'
    start_urls = ['http://www.ilknokta.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow=(r'/kitap/.*', ), unique=True), 'parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=(r'/.*', ), unique=True), ),
    )

    def parse_item(self, response):
		l = XPathItemLoader(item=BookItem(), response=response)
		l.add_xpath('name',     '//div[@class="divbaslik"]/@title')
		l.add_xpath('isbn',     '//td/text()', u'.*ISBN: ([0-9\-X]+)')
		l.add_xpath('author',   '//td[@class=\'yazart\']/a/text()')
		l.add_xpath('publisher','//a[@class=\'yayineviU\']/text()')
		l.add_xpath('price',    '//font[@class=\'fiyat\']/text()', u'([0-9,]+) TL')
		l.add_value('link', response.url)
		l.add_value('store', 6)
		return l.load_item()

SPIDER = IlknoktaSpider()
