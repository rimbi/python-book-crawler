# -*- coding: utf-8 -*-

import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawler.items import BookItem
from scrapy.contrib.loader import XPathItemLoader

class PandoraSpider(CrawlSpider):
    domain_name = 'pandora.com.tr'
    start_urls = ['http://www.pandora.com.tr/']

    rules = (
        Rule(SgmlLinkExtractor(allow=(r'/urun/.*',), unique=True), 'parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=(r'/.*', ), unique=True)),
    )

    def parse_item(self, response):
		l = XPathItemLoader(item=BookItem(), response=response)
		l.add_xpath('name',     '//span[@id="ContentPlaceHolderMainOrta_LabelAdi"]/text()')
		l.add_xpath('isbn',     '//span[@id="ContentPlaceHolderMainOrta_LabelIsbn"]/text()')
		l.add_xpath('author',   '//span[@id="ContentPlaceHolderMainOrta_LabelYazar"]/a/text()')
		l.add_xpath('publisher','//a[@id="ContentPlaceHolderMainOrta_HyperLinkYayinci"]/text()')
		l.add_xpath('price',    '//span[@class=\'fiyat\']/text()', u'(.*) TL')
		l.add_value('link', response.url)
		l.add_value('store', 4)
		return l.load_item()

SPIDER = PandoraSpider()
