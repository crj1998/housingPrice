from .SQL import MySQL
from housingPrice.items import HousingpriceItem

class hpPipeline(object):
    def process_item(self,item,spider):
        if isinstance(item,HousingpriceItem):
            name = item['city_name']
            ret = MySQL.isExist(name)
            if ret[0]==1:
                MySQL.updateContent(item['city_name'], item['city_price'], item['year'])
            else:
                MySQL.insertContent(item['city_name'],item['city_price'],item['year'])
