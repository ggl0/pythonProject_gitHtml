from pyecharts import options as opts
from pyecharts.charts import Grid, Line, Bar, Page,Kline
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType

import read_txt
import os


def local_data(data_type, fileName):
    file = './txtFile/' + fileName + '.txt'
    data_list = read_txt.get_list_fTxt(data_type, file)
    return data_list

def biasType(searchDate,biasLi=''):
    length = 60

    if biasLi == '':
        biasLi = local_data('bias_list', 'testData')
        date = local_data('date_list', 'testData')

        start_index = 0

        if searchDate != 0:
            searchDate = "'" + searchDate + "'"
            start_index = date.index(searchDate)

        biasLi = biasLi[start_index:(start_index+length)]
        date = date[start_index:(start_index+length)]
    else:
        biasLi = biasLi[0:length]


    x_tick = list(range(0,length))

    #drawFig(x_tick,biasLi)
    return x_tick,biasLi

def biasLine(x_,y_):
    lineB = (
        Line()
            .add_xaxis(x_)
            .add_yaxis("BIAS 3-6", y_, label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            opts.TitleOpts(title="BIAS Line", pos_right="5%"),
            opts.LegendOpts(is_show=False),

            # opts.DataZoomOpts(is_show=True,range_start=20,type_="slider",pos_left="5%")
        )
    )
    return lineB


def macdType(searchDate,macdpi=''):
    length = 60

    #local data
    if macdpi == '':
        macdpi = local_data('macdpi', 'testData')
        date = local_data('date_list', 'testData')
        start_index = 0
        if searchDate != 0:
            searchDate = "'" + searchDate + "'"
            start_index = date.index(searchDate)
        #print(start_index)

        macdpi = macdpi[start_index:(start_index+length)]
        date = date[start_index:(start_index+length)]
        #print(date)
        #print(len(date))
    else:
        macdpi = macdpi[0:length]

    x_tick = list(range(0, length))

    return x_tick,macdpi


def macdBar(x_,y_):
    barF = (
        Bar()
            .add_xaxis(x_)
            .add_yaxis("", y_, label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            opts.TitleOpts(title="MACD bar", pos_left="5%"),
            visualmap_opts=opts.VisualMapOpts(
                is_show=True,
                is_piecewise=True,  # 颜色分段
                pieces=[
                    {"min": 0, "color": 'red'},
                    {"max": 0, "color": 'green'}
                ],
                pos_top="0%",
                pos_right="0%"

            )

        )
    )

    return barF

def kAbbType(searchDate,highLi='',lowLi='',closeLi='',openLi='',HvLi='',MvLi='',LvLi=''):
    length = 60
    if highLi == '':
        highLi = local_data('high_list', 'testData')
        lowLi = local_data('low_list', 'testData')
        closeLi = local_data('close_list', 'testData')
        openLi = local_data('open_list', 'testData')

        HvLi = local_data('H_v', 'testData')
        MvLi = local_data('M_v', 'testData')
        LvLi = local_data('L_v', 'testData')

        date = local_data('date_list', 'testData')

        start_index = 0

        if searchDate != 0:
            searchDate = "'" + searchDate + "'"
            start_index = date.index(searchDate)
        #print(start_index)

        highLi = highLi[start_index:(start_index+length)]
        lowLi = lowLi[start_index:(start_index + length)]
        closeLi = closeLi[start_index:(start_index + length)]
        openLi = openLi[start_index:(start_index + length)]

        HvLi = HvLi[start_index:(start_index + length)]
        MvLi = MvLi[start_index:(start_index + length)]
        LvLi = LvLi[start_index:(start_index + length)]

        date = date[start_index:(start_index+length)]
    else:
        highLi = highLi[0:length]
        lowLi = lowLi[0:length]
        closeLi = closeLi[0:length]
        openLi = openLi[0:length]

        HvLi = HvLi[0:length]
        MvLi = MvLi[0:length]
        LvLi = LvLi[0:length]

    x_tick = list(range(0, length))
    price_data = kDataforChart(openLi,closeLi,lowLi,highLi,length)

    return x_tick,price_data,HvLi,MvLi,LvLi


def kDataforChart(o_l,c_l,l_l,h_l,length):
    list_all = [[0 for i in range(4)] for j in range(length)]
    for k in range(length):
        #0:open, 1:close, 2:low, 3:hight
        list_all[k][0] = o_l[k]
        list_all[k][1] = c_l[k]
        list_all[k][2] = l_l[k]
        list_all[k][3] = h_l[k]
    return list_all

def kLineD(x_,y_,hvLine,mvLine,lvLine):
    kL = (
        Kline()
        .add_xaxis(x_)
        .add_yaxis("kline",y_,itemstyle_opts=opts.ItemStyleOpts(
            color="#ec0000",
            color0="#00da3c",
            border_color="#8A0000",
            border_color0="#008F28",
        ),)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                    is_scale=True,
                    splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts = [opts.DataZoomOpts(type_="inside")],
            title_opts = opts.TitleOpts(title="Kline"),
        )
    )

    bbLine = (
        Line()
        .add_xaxis(x_)
        .add_yaxis(
            series_name="Hv",
            y_axis=hvLine,
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3,opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False)
        )
        .add_yaxis(
            series_name="Mv",
            y_axis=mvLine,
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False)
        )
        .add_yaxis(
            series_name="Lv",
            y_axis=lvLine,
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False)
        )
    )
    overlap_kline_line = kL.overlap(bbLine)
    return overlap_kline_line



def drawFig():
    isBiasLine = False
    isMACDBar = False
    x_line, y_line = biasType(0)
    x_bar, y_bar = macdType(0)

    if len(x_line) > 0 and len(y_line) > 0 and len(x_line) == len(y_line):
        line = biasLine(x_line, y_line)
        isBiasLine = True

    if len(x_bar) > 0 and len(y_bar) > 0 and len(x_bar) == len(y_bar):
        bar = macdBar(x_bar, y_bar)
        isMACDBar = True

    if isBiasLine and isMACDBar:
        '''grid = (
            Grid()
            .add(line,grid_opts=opts.GridOpts(pos_left="55%"))
            .add(bar, grid_opts=opts.GridOpts(pos_right="55%"))
            .render(path='first_bar1.html')
        )'''
        page = Page(layout=Page.SimplePageLayout)
        page.add(
            bar,
            line
        )
        page.render("Page_test.html")


    #line.render(path='first_bar.html')


kAbbType(0)