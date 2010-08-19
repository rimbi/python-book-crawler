# -*- coding: utf-8 -*-

import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawler.items import BookItem
from scrapy.contrib.loader import XPathItemLoader

class ImgeSpider(CrawlSpider):
    domain_name = 'imge.com.tr'
    start_urls = ['http://www.imge.com.tr/']

    rules = (
        Rule(SgmlLinkExtractor(allow=(r'product_info', ), unique=True), 'parse_item', follow=True),
    )

    def parse_item(self, response):
		l = XPathItemLoader(item=BookItem(), response=response)
		l.add_xpath('name',     '//td[@class=\'pageHeading\']/text()')
		l.add_xpath('isbn',     '//td[@class=\'main\']/text()', u'ISBN: ([0-9]+)')
		l.add_xpath('isbn',     '//td[@class=\'main\']/p/text()', u'ISBN: ([0-9]+)')
		l.add_xpath('author',   '//a[contains(@href, "/person.php")]/b/font/text()')
		l.add_xpath('publisher','//a[contains(@href, "manufacturers_id=")]/b/font/text()')
		l.add_xpath('price',    '//span[@class=\'productSpecialPrice\']/text()', u'(.*)TL')
		l.add_xpath('price',    '//td[@class=\'price\']/font[@class=\'special\']/text()', u'Fiyatı: (.*)TL')
		l.add_xpath('price',    '//td[@class=\'price\']/text()', u'(.*)TL')
		l.add_value('link', response.url)
		l.add_value('store', 1)
		return l.load_item()

SPIDER = ImgeSpider()
