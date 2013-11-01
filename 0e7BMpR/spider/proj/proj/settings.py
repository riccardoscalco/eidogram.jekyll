# Scrapy settings for terremoti project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'proj'

SPIDER_MODULES = ['proj.spiders']
NEWSPIDER_MODULE = 'proj.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'spider by eidogram.com'
ITEM_PIPELINES = ['proj.pipelines.ProjPipeline']

COOKIES_ENABLED = False
DOWNLOAD_DELAY = 1    # 1 sec of delay
