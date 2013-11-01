from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from proj.items import ProjItem


class ProjSpider(CrawlSpider):
    name = 'projspider'
    allowed_domains = ['camera.it']
    urls = 'http://www.camera.it/leg17/28?lettera='
    alfabeto = ['A','B','C','D','E','F','G','H','I','L','M','N','O','P','Q','R','S','T','U','V','Z','K','W','X','Y','J']
    start_urls = [urls + i for i in alfabeto]
    #start_urls = ['http://www.camera.it/leg17/28?lettera=A']
    restr_xpath = '//*[@id="composizioneOrgano"]/div[3]'

    rules = (
            Rule(SgmlLinkExtractor(allow=['idPersona','tipoPersona'], restrict_xpaths=restr_xpath), callback='parse_item'),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = ProjItem()
        s = hxs.select('//*[@id="schedaPersonale"]/div[2]/div[1]/text()[1]').extract()[0].split()
        i['Cognome'] = s[0] 
        i['Nome'] = s[1]
        s = hxs.select('//*[@id="schedaPersonale"]/div[2]/div[2]').extract()[0]
        if 'Nato' in s:
            i['Sesso'] = 'M'
        elif 'Nata' in s:
            i['Sesso'] = 'F'
        s = hxs.select('//*[@id="schedaPersonale"]/div[2]/div[2]/text()[2]').extract()[0].split()
        i['Anno_nascita'] = s[-1] 
        s = hxs.select('//*[@id="schedaPersonale"]/div[2]/div[2]/text()[3]').extract()[0]
        i['Titolo'] = s.split(';')[0] 
        i['Gruppo'] = hxs.select('//*[@id="schedaPersonale"]/div[2]/div[3]/div/text()[3]').extract()[0]
        print i
        return i
