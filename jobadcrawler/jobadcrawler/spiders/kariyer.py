from re import match
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import BaseSgmlLinkExtractor
from jobadcrawler.items import JobItem
from scrapy.contrib.loader import XPathItemLoader

def _url_filter(url):
	if match('/ilan/.*', url) or match('/jobSearch/.*', url): return url

class KariyerSpider(CrawlSpider):

	domain_name = 'kariyer.net'
	start_urls = ['http://www.kariyer.net/index_sb.kariyer?sec=02']
	rules = [Rule(BaseSgmlLinkExtractor(process_value=_url_filter), 'parse_job')]

	def parse_job(self, response):
		l = XPathItemLoader(item=JobItem(), response=response)
		l.add_xpath('title', '/html/head/meta[@name=\'keywords\']/@content')
		l.add_xpath('desc', '/html/head/meta[@name=\'description\']/@content')
		l.add_value('link', response.url)
		return l.load_item()

myspider = KariyerSpider();
