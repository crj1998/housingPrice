import scrapy
import lxml.etree
from scrapy.http import Request
from housingPrice.items import HousingpriceItem

class hpSpider(scrapy.Spider):
    name = 'housingPrice'
    allowed_domains = ['mobile.anjuke.com']

    def start_requests(self):
        for year in (2018,2017,-1):
            url = 'https://mobile.anjuke.com/fangjia/quanguo%s/'%str(year)
            yield Request(url,self.parse,meta={'year':str(year)})

    def parse(self, response):
        html = lxml.etree.HTML(response.text)
        city_list = html.xpath("//ul[@class='listseo-item']/li")
        for city in city_list:
            name = city.xpath('a/span')[0].text[5:-2]
            url = city.xpath('a')[0].get('href')
            #name_en = url.split('/')[-2][:-4]
            yield Request(url,callback=self.get_month,meta={'name':name,'year':response.meta['year']})

    def get_month(self, response):
        html = lxml.etree.HTML(response.text)
        months = html.xpath("//ul[@class='listseo-item']")[0].xpath('li')
        month_price={'01': None, '02': None, '03': None, '04': None, '05': None, '06': None, '07': None, '08': None, '09': None, '10': None, '11': None, '12': None}
        for m in months:
            month = m.xpath("a/span[@class='item-1']")[0].text[-6:-3]
            price = m.xpath("a/span[@class='item-2']")[0].text[:-3]
            try:
                month_price[month] = int(price)
            except:
                pass
        item = HousingpriceItem()
        item['city_name'] = response.meta['name']
        item['year'] = response.meta['year']
        item['city_price'] = month_price
        yield item