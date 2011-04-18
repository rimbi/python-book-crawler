# -*- coding: utf-8 -*-

import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawler.items import BookItem
from scrapy.contrib.loader import XPathItemLoader

class KitapyurduSpider(CrawlSpider):
    domain_name = 'kitapyurdu.com'
    start_urls = ['http://www.kitapyurdu.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow=(r'kitap/', ), deny=(r'changeCurrency', ), unique=True), 'parse_item', follow=True),
    )

    def parse_item(self, response):
		l = XPathItemLoader(item=BookItem(), response=response)
		l.add_xpath('name',     '//span[@class=\'kitapismi\']/text()')
		l.add_xpath('isbn',     '//span[@class=\'normalkucuk\']/text()', u'ISBN:([0-9X]+)')
		l.add_xpath('author',   '//span/a[contains(@href, "/yazar/")]/text()')
		l.add_xpath('publisher','//span/a[contains(@href, "/yayinevi/")]/text()')
		l.add_xpath('price',    '//td/text()', u'Kitapyurdu Fiyatı:\s([0-9,]*).*')
		l.add_value('link', response.url)
		l.add_value('store', 3)
		return l.load_item()

SPIDER = KitapyurduSpider()
