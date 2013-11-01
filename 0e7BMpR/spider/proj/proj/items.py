# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ProjItem(Item):
    Cognome = Field()
    Nome = Field()
    Sesso = Field()
    Anno_nascita = Field()
    Titolo = Field()
    Gruppo = Field()
    pass
