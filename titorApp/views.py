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
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import timedelta
import json
import jsm
import datetime
import os.path
import JsmWriteFile
import sys,os
import glob
import re

# Create your views here.
##############################
#
# nikkei average = 998407
#
##############################
CORP_CD = 998407
FILE_PATH = 'titorApp/price_data/'
BACH_PATH = '/management/commands'
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + BACH_PATH)
print os.path.dirname(os.path.abspath(__file__)) + BACH_PATH


class JsmGetPrice():
    def __init__(self,corp_cd,start_date,end_date):
        self.corp_cd = corp_cd    
        self.start_date = start_date    
        self.end_date = end_date 
        self.close_dict = {}
        self.close_list = []
        self.date_list = []

        file_name = FILE_PATH + str(self.corp_cd) + '_' + str(self.end_date) + '.json'
        if os.path.exists(file_name):
            #file exists
            print "file exit!!! "
            print glob.glob(FILE_PATH + '*')

        else:
            print "file not exist"
            #file not exists
            #oldfile delite
            print glob.glob(FILE_PATH + '*')
            for i in glob.glob(FILE_PATH + '*'):
                os.remove(i)           
 
            #file create
            jsm = JsmWriteFile.JsmPriceFileCreate(self.corp_cd,self.start_date,self.end_date)
            print "file make"
            jsm.json_write()

        f = open(file_name,'r')
        self.close_dict = json.load(f)
        f.close()
        for k,v in sorted(self.close_dict.items()):
            v = int(v)
            self.close_list.append(v)
            self.date_list.append(k.encode('utf-8'))
        
    def get_price(self):
        return self.close_list

    def get_date(self):
        taihi = "a"
        d_list = []
        for d in self.date_list:
            d = d[0:7]
            if taihi == d:
                d_list.append(" ") 
            else:
                d_list.append(d)
            taihi = d 
        print d_list
        return d_list

    def month_get_price(self):
        print self.close_list
        month_price_list = []
        month_data_len = len(self.close_list) - 20
        month_price_list = self.close_list[month_data_len:]
        return month_price_list

    def month_get_date(self):
        print self.date_list
        month_date_list = []
        month_data_len = len(self.date_list) - 20
        month_date_list = self.date_list[month_data_len:]
        return month_date_list



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
        old_day = today - datetime.timedelta(days=365) 
        start_date = old_day
        end_date = today
        get_jsm = JsmGetPrice(CORP_CD,start_date,end_date)  

        #get_date
        date = get_jsm.get_date()
        #get_price
        close_price = get_jsm.get_price()
        
        return [date, close_price]



class MonthData(TemplateView):
    template_name = "titor/graph.html"

    def get_context_data(self, **kwargs):
        print "Month get"
        #context = super(AnalyticsIndexView, self).get_context_data(**kwargs)
        context = super(MonthData, self).get_context_data(**kwargs)
        date, close_price =  self.stock_price_registrations()
        #context['stock_registrations'] = self.stock_price_registrations()
        context['stock_registrations'] = close_price
        context['date_registrations'] = date
        return context

    def stock_price_registrations(self):

        #generate instance
        
        today = datetime.date.today()
        old_day = today - datetime.timedelta(days=365)
        start_date = old_day
        end_date = today
        get_jsm = JsmGetPrice(CORP_CD,start_date,end_date)  

        #get_date
        date = get_jsm.month_get_date()
        #date = get_jsm.get_date()
        #get_price
        close_price = get_jsm.month_get_price()
        #close_price = get_jsm.get_price()
        
        print get_jsm.month_get_date()
        print get_jsm.month_get_price()
        return [date, close_price]

