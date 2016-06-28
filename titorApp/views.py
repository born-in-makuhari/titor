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
import jsm
import datetime
import re
import arrow
# Create your views here.


##############################
#
# nikkei average = 998407
#
##############################
CORP_CD = 998407

"""

class ColorsView(TemplateView):
    template_name = 'colors.html'

    def get_context_data(self, **kwargs):
        data = super(ColorsView, self).get_context_data(**kwargs)
        data['colors'] = islice(next_color(), 0, 50)
        return data

class ChartMixin(object):

    def test(self):
        print "test"
        return 0 

    def get_labels(self):
        #return ["January", "February", "March", "April", "May", "June", "July"]
        get_jsm = JsmGetPrice(CORP_CD,START_DATE,END_DATE)
        #get_jsm = GET_JSM
        date = get_jsm.get_date()
        return date
        #return ["1","2","3","4","5","6","7","8"]

    def get_data(self):
        def data():
            return [randint(0, 100) for x in range(7)]

        #return [data() for x in range(3)]
        get_jsm = JsmGetPrice(CORP_CD,START_DATE,END_DATE)
        close_price = get_jsm.get_price()     
        return [close_price]

    def get_colors(self):
        colors = COLORS[:]
        shuffle(colors)
        return next_color(colors)



class ColumnHighChartJSONView(ChartMixin, BaseColumnsHighChartsView):
    title = _('Column Highchart test')
    yUnit = '%'
    providers = ['All']
    credits = {"enabled": False}

    def get_data(self):
        return [super(ColumnHighChartJSONView, self).get_data()]



class LineChartJSONView(ChartMixin, BaseLineChartView):
    pass

class LineHighChartJSONView(ChartMixin, HighchartPlotLineChartView):
    # special - line charts credits are personalized
    credits = {
        'enabled': True,
        'href': 'http://example.com',
        'text': 'Novapost Team',
    }

class PieHighChartJSONView(ChartMixin, HighChartPieView):
    pass


class DonutHighChartJSONView(ChartMixin, HighChartDonutView):
    pass
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

    def get_date(self):
        return self.date_list


#class AnalyticsIndexView(TemplateView):
class AboutView(TemplateView):
    template_name = "titor/graph.html"

    def get_context_data(self, **kwargs):
        #context = super(AnalyticsIndexView, self).get_context_data(**kwargs)
        context = super(AboutView, self).get_context_data(**kwargs)
        context['30_day_registrations'] = self.thirty_day_registrations()
        return context

    def thirty_day_registrations(self):

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

        date = [1,2,3,4,5]
        price_dict = {"price":close_price,"date_":date}
        
        return price_dict


