from pyecharts import options as opts
from pyecharts.charts import Grid, Line, Bar, Page,Kline
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType

import read_txt
import os
import futureBias

isDebug = False


def local_data(data_type, fileName):
    file = './txtFile/' + fileName + '.txt'
    data_list = read_txt.get_list_fTxt(data_type, file)
    return data_list

###########################################################################################
######################################BIAS#################################################
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

def biasLine(x_,y_,num):
    titleName = num + "  BIAS Line"
    lineB = (
        Line()
            .add_xaxis(x_)
            .add_yaxis("BIAS 3-6", y_, label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            opts.TitleOpts(title=titleName, pos_left="5%"),
            opts.LegendOpts(is_show=False),

            # opts.DataZoomOpts(is_show=True,range_start=20,type_="slider",pos_left="5%")
        )
    )

    return lineB




#draw bias future line, two days up
def drawBiasFLine_multi(searchDate,days,isSingleTest,closeList,num):
    titleName = num + "  BIAS Line"
    isTest = False
    isPrePrice = False
    isDraw = False
    testL = ''
    isAddXline = False



    c_p = list()
    fbias = futureBias.calFuture()
    if isSingleTest:
        fbiasC_p = futureBias.singleTestData()

        c_p = fbiasC_p.test()
    else:
        c_p = closeList
    if isDebug: print('c_p=', c_p)

    limit_var = 0
    limit_var_ = 0
    i = 0
    while i < (days):
        limit_var = limit_var + 3**i
        i += 1
    if days - 1 > 0:
        for i in range(days-1):
            limit_var_ = limit_var_ + 3**i
    else:
        limit_var_ = 0

    if isTest and isDebug: print('limit_var=',limit_var,', limit_var_=',limit_var_)

    #os.system("pause")
    pre_index = 0

    xdays = list()
    multiLine = Line()
    for j in range(limit_var):
        index = str(j)

        locals()['hBiasL_' + index] = []
        locals()['mBiasL_' + index] = []
        locals()['lBiasL_' + index] = []

        locals()['c_p_' + index] = fbias.addTodayCp(c_p)

        if j != 0:
            if j % 3 == 0:
                pre_index = int((j / 3) - 1)
                #if isDebug: print('pre_index=',pre_index)
                prePrice_L = round((locals()['c_p_' + str(pre_index)][0] - round((locals()['c_p_' + str(pre_index)][0] / 10),2)),2)
                if isDebug: print('prePrice_L=',prePrice_L)
                c_p = locals()['c_p_' + str(pre_index)]
                locals()['c_p_' + index] = fbias.addTodayCp(c_p,prePrice_L)
            elif j % 3 == 1:
                pre_index = int(j / 3)
                #if isDebug: print('pre_index=', pre_index)
                isPrePrice = True
                prePrice_H = round((locals()['c_p_' + str(pre_index)][0] + round((locals()['c_p_' + str(pre_index)][0] / 10),2)),2)
                c_p = locals()['c_p_' + str(pre_index)]
                locals()['c_p_' + index] = fbias.addTodayCp(c_p,prePrice_H)
            elif j % 3 == 2:
                pre_index = int(j / 3)
                #if isDebug: print('pre_index=', pre_index)
                prePrice_M = locals()['c_p_' + str(pre_index)][0]
                c_p = locals()['c_p_' + str(pre_index)]
                locals()['c_p_' + index] = fbias.addTodayCp(c_p,prePrice_M)





        if isDebug: print('index=',index,', c_p=',locals()['c_p_' + index][0:10])
        locals()['hBiasL_' + index], locals()['mBiasL_' + index],locals()['lBiasL_' + index] = fbias.futureList(locals()['c_p_' + index])

        limit_len = len(locals()['hBiasL_' + index])
        if limit_len > 60:
            limit_len = 60


        if not isAddXline:
            xdays = list(range(0,limit_len))
            multiLine.add_xaxis(xdays)
            isAddXline = True

        locals()['hBiasL_' + index] = locals()['hBiasL_' + index][0:limit_len]
        locals()['mBiasL_' + index] = locals()['mBiasL_' + index][0:limit_len]
        locals()['lBiasL_' + index] = locals()['lBiasL_' + index][0:limit_len]
        if isDebug: print('j=', j, ', limit_var_=', limit_var_, ', index=',index)
        if j >= limit_var_:
            multiLine.add_yaxis("BIAS_3-6_" + index,locals()['hBiasL_' + index],
                                label_opts=opts.LabelOpts(is_show=False))
            multiLine.add_yaxis("BIAS_3-6_" + index, locals()['mBiasL_' + index],
                                label_opts=opts.LabelOpts(is_show=False))
            multiLine.add_yaxis("BIAS_3-6_" + index, locals()['lBiasL_' + index],
                                label_opts=opts.LabelOpts(is_show=False))
            isDraw = True
        if isDebug: print(locals()['hBiasL_' + index][0:10])
        del locals()['hBiasL_' + index]
        del locals()['mBiasL_' + index]
        del locals()['lBiasL_' + index]
    if isDraw:
        multiLine.set_global_opts(
            opts.TitleOpts(title=titleName, pos_left="5%"),
            opts.LegendOpts(is_show=True))
        #multiLine.render("test.html")
    return multiLine




###########################################################################################
###########################################################################################

###########################################################################################
#########MACD############MACD#################MACD######################MACD###############
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


def macdBar(x_,y_,num):
    titleName = num + "  MACD bar"
    barF = (
        Bar()
            .add_xaxis(x_)
            .add_yaxis("", y_, label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            opts.TitleOpts(title=titleName, pos_left="5%"),
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
###########################################################################################
###########################################################################################


###########################################################################################
################KLINE#########KLINE##########KLINE#############KLINE#######################
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

def kLineD(x_,y_,hvLine,mvLine,lvLine,num):
    titleName = num + "  Kline"
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
            datazoom_opts = [opts.DataZoomOpts(type_="inside",range_start=0)],
            title_opts = opts.TitleOpts(title=titleName),
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
###########################################################################################
###########################################################################################
def drawHtml(num='',macdpi='',biasList='',highLi='',lowLi='',closeLi='',openLi='',HvLi='',MvLi='',LvLi='',fileName='hisBBands'):
    print('num=',num,', fileName=',fileName)
    num = str(num)
    filePath = fileName + '/' + str(num) + ".html"
    normalBias = False
    isBiasLine = False
    isMACDBar = False
    isK = False
    if normalBias:
        x_line, y_line = biasType(0,biasList)
    else:
        line = drawBiasFLine_multi(0, 2, False, closeLi, num)
        isBiasLine = True

    x_bar, y_bar = macdType(0,macdpi)
    x_k, y_k, hv_l, mv_l, lv_l = kAbbType(0,highLi,lowLi,closeLi,openLi,HvLi,MvLi,LvLi)

    if normalBias:
        if len(x_line) > 0 and len(y_line) > 0 and len(x_line) == len(y_line):
            line = biasLine(x_line, y_line, num)
            isBiasLine = True

    if len(x_bar) > 0 and len(y_bar) > 0 and len(x_bar) == len(y_bar):
        bar = macdBar(x_bar, y_bar, num)
        isMACDBar = True

    if len(x_k) > 0 and len(y_k) > 0 and len(x_k) == len(y_k):
        kDbar = kLineD(x_k, y_k, hv_l, mv_l, lv_l, num)
        isK = True

    if isDebug: print("isBiasLine=",isBiasLine,", isMACDBar=", isMACDBar,", isK=", isK)
    if isBiasLine and isMACDBar and isK:
        page = Page(layout=Page.SimplePageLayout)
        page.add(
            kDbar,
            bar,
            line
        )
        page.render(filePath)
    else:
        print("num=",num,', has some error! need check!')
        os.system("pause")



def drawHtmlSingleTest():
    num = 'testnum1101'
    normalBias = False
    isBiasLine = False
    isMACDBar = False
    isK = False
    if normalBias:
        x_line, y_line = biasType(0)
    else:
        line = drawBiasFLine_multi(0,2,True,'',num)
        isBiasLine = True

    x_bar, y_bar = macdType(0)
    x_k, y_k, hv_l, mv_l, lv_l = kAbbType(0)


    if normalBias:
        if len(x_line) > 0 and len(y_line) > 0 and len(x_line) == len(y_line):
            line = biasLine(x_line, y_line,num)
            isBiasLine = True

    if len(x_bar) > 0 and len(y_bar) > 0 and len(x_bar) == len(y_bar):
        bar = macdBar(x_bar, y_bar,num)
        isMACDBar = True

    if len(x_k) > 0 and len(y_k) > 0 and len(x_k) == len(y_k):
        kDbar = kLineD(x_k, y_k, hv_l, mv_l, lv_l,num)
        isK = True

    if isDebug: print("isBiasLine=",isBiasLine,", isMACDBar=", isMACDBar,", isK=", isK)
    if isBiasLine and isMACDBar and isK:
        '''grid = (
            Grid()
            .add(line,grid_opts=opts.GridOpts(pos_left="55%"))
            .add(bar, grid_opts=opts.GridOpts(pos_right="55%"))
            .render(path='first_bar1.html')
        )'''
        page = Page(layout=Page.SimplePageLayout)
        page.add(
            kDbar,
            bar,
            line
        )
        page.render("Page_test.html")


    #line.render(path='first_bar.html')

if __name__ == '__main__':
    drawHtmlSingleTest()
    # drawBiasFLine_multi(0,2,True,'')
