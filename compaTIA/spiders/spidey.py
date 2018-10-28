from scrapy.spider import BaseSpider
#from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.http import FormRequest, Request
import re
#import scrapy
import math
import sys
import base64
import time
import urllib3
import certifi


reload(sys)
sys.setdefaultencoding("utf_8")
sys.getdefaultencoding()

from compaTIA.items import CompatiaItem

class mySpider(BaseSpider):
    name = "compaTIA"

    allowed_domains = ["comptia.org"]
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED', # Force certificate check.
        ca_certs=certifi.where(),  # Path to the Certifi bundle.
    )

    start_urls = ['https://www.comptia.org/']

    def parse(self, response):

        viewState = response.selector.xpath("//input[@id='__VIEWSTATE']/@value").extract().pop(0)
        viewStateGenerator = response.selector.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract().pop(0)
        eventValidation = response.selector.xpath("//input[@id='__EVENTVALIDATION']/@value").extract().pop(0)

        return FormRequest(
            "https://www.comptia.org/",
            formdata = {'ctl04_TSSM':'',
                        '__EVENTTARGET':'',
                        '__EVENTARGUMENT':'',
                        '__VIEWSTATE':viewState,
                        '__VIEWSTATEGENERATOR':viewStateGenerator,
                        '__EVENTVALIDATION':eventValidation,
                        'ctl00$TopNavigation$txtSearchText':'',
                        'ctl00$TopNavigation$TopNavigation_LoginBox$txtUsername':'dina@saasmax.com',
                        'ctl00$TopNavigation$TopNavigation_LoginBox$txtPassword':'matrix7!',
                        'ctl00$TopNavigation$TopNavigation_LoginBox$btnLogin':'Submit',
                        'ctl00$txtSearchText':''},
            callback = self.after_login
        )

    def after_login(self, response):

        url="https://www.comptia.org/insight-tools/individual-directory/"
        print "requesting"
        myRequest = Request(url, callback = self.searchPage, dont_filter=True)
        yield myRequest



    def searchPage(self, response):


        file = open('urls.txt','r')
        urls = file.readlines()
        for url in urls:
            url = url[:-1]
            if "https://www.comptia.org" in url:
                myRequest = Request(str(url), callback = self.ItemPage)
                yield myRequest
            else:
                myRequest = Request("https://www.comptia.org" + str(url), callback = self.ItemPage)
                yield myRequest


    def ItemPage(self, response):


        item = CompatiaItem()

        organization = response.selector.xpath("//div[@class='top']/h2/span/text()").extract()
        item['Organization'] = organization

        memberPath = "//span[@id='LeftColumn_C001_lbl_MemberType']/text()"
        member = response.selector.xpath(memberPath).extract()
        item['MemberType'] = member

        websitePath = "//span[@id='LeftColumn_C001_lbl_Website']/a/text()"
        website = response.selector.xpath(websitePath).extract()
        item['Website'] = website

        namePath = "//span[@id='LeftColumn_C001_lbl_Name']/text()"
        name = response.selector.xpath(namePath).extract()
        if name != []:
            name = name.pop(0)
            name = name.split()
            item['FirstName'] = name.pop(0)
            item['LastName'] = ' '.join(name)

        TitlePath = "//span[@id='LeftColumn_C001_lbl_Title']/text()"
        Title = response.selector.xpath(TitlePath).extract()
        item['Title'] = Title

        addressPath = "//span[@id='LeftColumn_C001_lbl_Address']/text()"
        address = response.selector.xpath(addressPath).extract()
        item['Address'] = address

        phonePath = "//span[@id='LeftColumn_C001_lbl_Phone']/text()"
        phone = response.selector.xpath(phonePath).extract()
        item['Phone'] = phone

        return item
