# Scrapy settings for dmoz project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
# Or you can copy and paste them from where they're defined in Scrapy:
# 
#     scrapy/conf/default_settings.py
#

BOT_NAME = 'jobadcrawler'
BOT_VERSION = '0.1'

SPIDER_MODULES = ['jobadcrawler.spiders']
NEWSPIDER_MODULE = 'jobadcrawler.spiders'
DEFAULT_ITEM_CLASS = 'jobadcrawler.items.JobItem'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.A.B.C Safari/525.13'
#ITEM_PIPELINES = ['jobadcrawler.pipelines.XmlExportPipeline']
ITEM_PIPELINES = ['jobadcrawler.pipelines.DbExportPipeline']
CONCURRENT_REQUESTS_PER_SPIDER = 1
DOWNLOAD_DELAY = 2
