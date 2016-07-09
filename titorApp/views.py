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

        else:
            #file not exists
            #file create
            print "file not exist"
            jsm = JsmWriteFile.JsmPriceFileCreate(self.corp_cd,self.start_date,self.end_date)
            print "file make"
            jsm.json_write()

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
