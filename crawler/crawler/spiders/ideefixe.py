# -*- coding: utf-8 -*-

import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawler.items import BookItem
from scrapy.contrib.loader import XPathItemLoader

class IdefixSpider(CrawlSpider):
    domain_name = 'idefix.com'
    start_urls = ['http://www.idefix.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow=(r'/kitap/', )), 'parse_item', follow=True),
    )

    def parse_item(self, response):
		l = XPathItemLoader(item=BookItem(), response=response)
		l.add_xpath('name',     '//div[@class=\'boxTanimisim\']/div/text()')
		l.add_xpath('isbn',     '//div[@id=\'tanitimbox\']/text()', u'.*ISBN : ([0-9]+)')
		l.add_xpath('author',   '//div[@class=\'boxTanimVideo\']/a/text()')
		l.add_xpath('publisher','//h3[@class=\'boxTanimyayinevi\']/a/b/text()')
		l.add_xpath('price',    '//b[@class=\'pricerange\']/text()', u'\s*(.*) TL \(KDV Dahil\)')
		l.add_value('link', response.url)
		l.add_value('store', 2)
		return l.load_item()

SPIDER = IdefixSpider()
