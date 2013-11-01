# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import pickle

class ProjPipeline(object):
    def open_spider(self,spider):
        self.result = []
        return None
    def process_item(self, item, spider):
        self.result.append(dict(item))
        return None
    def close_spider(self,spider):
        f = open('deputati.pickle','w')
        pickle.dump(self.result,f)
        f.close()
        
