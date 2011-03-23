# -*- coding: utf-8 -*-

import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawler.items import BookItem
from scrapy.contrib.loader import XPathItemLoader

class NetkitapSpider(CrawlSpider):
    domain_name = 'netkitap.com'
    start_urls = ['http://www.netkitap.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow=(r'/kitap-', ), unique=True), 'parse_item', follow=True),
    )

    def parse_item(self, response):
		l = XPathItemLoader(item=BookItem(), response=response)
		l.add_xpath('name',     '//h1[@class=\'kitapad14pnt\']/b/text()')
		l.add_xpath('isbn',     '//span[@class=\'kunye\']/text()', u'ISBN: ([0-9\-X]+)')
		l.add_xpath('author',   '//span[@class=\'yazarad12pnt\']/a/span[@class=\'yazarad12pnt\']/text()')
		l.add_xpath('publisher','//h3[@class=\'kapakyazisi\']/b/font/a/text()')
		l.add_xpath('price',    '//span[@class=\'kapakyazisi\']/font/b/text()', u'(.*) TL')
		l.add_xpath('price',    '//span[@class=\'kapakyazisi\']/b/text()', u'(.*) TL')
		l.add_value('link', response.url)
		l.add_value('store', 5)
		return l.load_item()

SPIDER = NetkitapSpider()
