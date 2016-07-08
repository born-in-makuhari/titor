# -*- coding:utf-8 -*-

from django.shortcuts import render
from random import shuffle, randint
from itertools import islice
from django.http import HttpResponse
from django.template import Context, loader
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from chartjs.colors import next_color, COLORS
from chartjs.views.columns import BaseColumnsHighChartsView
from chartjs.views.lines import BaseLineChartView, HighchartPlotLineChartView
from chartjs.views.pie import HighChartPieView, HighChartDonutView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import timedelta
import json
import jsm
import datetime
# Create your views here.
##############################
#
# nikkei average = 998407
#
##############################
CORP_CD = 998407
FILE_PATH = 'titorApp/price_data/'

class JsmGetPrice():
    def __init__(self,corp_cd,start_date,end_date):
        self.corp_cd = corp_cd    
        self.start_date = start_date    
        self.end_date = end_date 
        self.close_dict = {}
        self.close_list = []
        self.date_list = []


        file_name = FILE_PATH + str(self.corp_cd) + '_' + str(self.end_date) + '.json'
        f = open(file_name,'r')
        self.close_dict = json.load(f)
        f.close()
        for k,v in sorted(self.close_dict.items()):
            self.close_list.append(v)
            self.date_list.append(k.encode('utf-8'))

    def get_price(self):
        return self.close_list

    def get_date(self):
        return self.date_list
"""
class JsmGetPrice():
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
        #print str(pricedata_eachday.date).replace(' 00:00:00','')
            self.close_dict[str(pricedata_eachday.date).replace(' 00:00:00','')] = pricedata_eachday.close
        for k,v in sorted(self.close_dict.items()):
            self.close_list.append(v)
            self.date_list.append(k)

    def get_price(self):
        return self.close_list
        #return 0

    def get_date(self):
        return self.date_list
        #return 0

"""


#class AnalyticsIndexView(TemplateView):
class AboutView(TemplateView):
    template_name = "titor/graph.html"

    def get_context_data(self, **kwargs):
        #context = super(AnalyticsIndexView, self).get_context_data(**kwargs)
        context = super(AboutView, self).get_context_data(**kwargs)
        date, close_price =  self.stock_price_registrations()
        #context['stock_registrations'] = self.stock_price_registrations()
        context['stock_registrations'] = close_price
        context['date_registrations'] = date
        return context

    def stock_price_registrations(self):

        #generate instance
        today = datetime.date.today()
        old_day = today - datetime.timedelta(days=30) 
        start_date = old_day
        end_date = today
        get_jsm = JsmGetPrice(CORP_CD,start_date,end_date)  
          

        #get_date
        date = get_jsm.get_date()
        #get_price
        close_price = get_jsm.get_price()
        
        return [date, close_price]
