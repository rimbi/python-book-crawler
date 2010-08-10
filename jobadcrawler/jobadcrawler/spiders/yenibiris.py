from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from jobadcrawler.items import JobItem
from scrapy.contrib.loader import XPathItemLoader

class YenibirisSpider(CrawlSpider):

	domain_name = 'yenibiris.com'
	start_urls = ['http://www.yenibiris.com/Is_Ilanlari/Son_Bir_Ay']
	rules = [Rule(SgmlLinkExtractor(allow=['/.+ilan']), 'parse_job')]

	def parse_job(self, response):
		l = XPathItemLoader(item=JobItem(), response=response)
		l.add_xpath('title', '//td[@class=\'adPosition\']/h2/text()')
		l.add_xpath('desc', '//td[@class=\'adAciklama\']/text()')
		l.add_value('link', response.url)
		return l.load_item()
			
myspider = YenibirisSpider();
