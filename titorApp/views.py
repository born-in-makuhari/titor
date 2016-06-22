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
import jsm
import datetime
import re
# Create your views here.

#GLOBAL
CORP_CD = 998407
START_DATE = datetime.date(2015, 5, 27)
END_DATE = datetime.date(2016, 6, 17)
print "GLOBAL"
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
        """Return 7 labels."""
        #return ["January", "February", "March", "April", "May", "June", "July"]
        get_jsm = JsmGetPrice(CORP_CD,START_DATE,END_DATE)
        #get_jsm = GET_JSM
        date = get_jsm.get_date()
        return date
        #return ["1","2","3","4","5","6","7","8"]

    def get_data(self):
        """Return 3 random dataset to plot."""
        def data():
            """Return 7 randint between 0 and 100."""
            return [randint(0, 100) for x in range(7)]

        #return [data() for x in range(3)]
        get_jsm = JsmGetPrice(CORP_CD,START_DATE,END_DATE)
        close_price = get_jsm.get_price()     
        return [close_price]

    def get_colors(self):
        """Return a new shuffle list of color so we change the color
        each time."""
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


class AboutView(TemplateView):
    template_name = "titor/graph.html"

class JsmGetPrice():
    def __init__(self,corp_cd,start_date,end_date):
        self.corp_cd = corp_cd    
        self.start_date = start_date    
        self.end_date = end_date    
        q = jsm.Quotes()
        self.close_dict = {}
        self.pricedata = q.get_historical_prices(corp_cd, jsm.DAILY, start_date, end_date)
        for pricedata_eachday in self.pricedata:
        #print str(pricedata_eachday.date).replace(' 00:00:00','')
            self.close_dict[str(pricedata_eachday.date).replace(' 00:00:00','')] = pricedata_eachday.close

    def get_price(self):
        close_list = []
        for k,v in sorted(self.close_dict.items()):
            close_list.append(v)

        return close_list

    def get_date(self):
        #pricedata = q.get
        #print self.pricedata
        i = 0
        day_list = []
        print len(self.pricedata)
        for pricedata_eachday in self.pricedata:
            day_list.append(str(pricedata_eachday.date).replace(' 00:00:00',''))
        
        print day_list
        return day_list



line_chart_json = LineChartJSONView.as_view()
line_highchart_json = LineHighChartJSONView.as_view()
pie_highchart_json = PieHighChartJSONView.as_view()
donut_highchart_json = DonutHighChartJSONView.as_view()
