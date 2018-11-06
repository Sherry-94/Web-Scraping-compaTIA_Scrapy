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
