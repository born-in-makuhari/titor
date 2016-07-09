from django.core.management.base import BaseCommand
import jsm
from datetime import timedelta
import json
import jsm
import datetime

##############################
#
# nikkei average = 998407
#
##############################
CORP_CD = 998407
FILE_PATH = 'titorApp/price_data/'

class JsmPriceFileCreate():
    def __init__(self,corp_cd,start_date,end_date):
        q = jsm.Quotes()
        self.corp_cd = corp_cd    
        self.start_date = start_date    
        self.end_date = end_date    
        self.close_dict = {}
        self.pricedata = q.get_historical_prices(corp_cd, jsm.DAILY, start_date, end_date)
        self.close_list = []
        self.date_list = []

        for pricedata_eachday in self.pricedata:
            self.close_dict[str(pricedata_eachday.date).replace(' 00:00:00','')] = pricedata_eachday.close
        
        for k,v in sorted(self.close_dict.items()):
            self.close_list.append(v)
            self.date_list.append(k)


    def json_write(self):
        print "file make start"
        file_name = FILE_PATH + str(self.corp_cd) + '_' + str(datetime.date.today()) + '.json'
        f = open(file_name,'w')
        json.dump(self.close_dict,f)
        f.close()
        return 0


    def get_price(self):
        return self.close_list

    def get_date(self):
        return self.date_list
