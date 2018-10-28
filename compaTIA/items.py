# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CompatiaItem(Item):
    Organization = Field()
    MemberType = Field()
    Website = Field()
    FirstName = Field()
    LastName = Field()
    Title = Field()
    Address = Field()
    Phone = Field()
