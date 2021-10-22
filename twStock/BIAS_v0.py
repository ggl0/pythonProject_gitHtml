import math

def list_strTofloat(str_list):
    float_list = list()
    for i in range(len(str_list)):
        float_list.append(float(str_list[i]))

    if len(float_list) == len(str_list):
        return float_list
    else:
        return str_list

def cal_36(close_p):
    list_36 = list()
    close_p = list_strTofloat(close_p)
    for i in range(len(close_p)):
        if (i + 6) <= len(close_p):
            value_36 = three_six_func(close_p[i],close_p[i+1],close_p[i+2],close_p[i+3],close_p[i+4],close_p[i+5])
            list_36.append(value_36)
    return list_36


# BIAS calculat
def three_six_func(p1, p2, p3, p4, p5, p6):
    three_2 = math.floor(((p1 + p2 + p3) / 3)*10000)
    three_3 = three_2 / 10000
    if (p1 - three_3) == 0 or three_3 == 0:
        three_v1 = 0
        three_v2 = 0
    else:
        three_v1 = math.floor(((p1 - three_3) / three_3)*10000)
        three_v2 = three_v1 / 10000

    six_2 = math.floor(((p1 + p2 + p3 + p4 + p5 + p6) / 6)*10000)
    six_3 = six_2 / 10000
    if (p1 - six_3) == 0 or six_3 == 0:
        six_v1 = 0
        six_v2 = 0
    else:
        six_v1 = math.floor(((p1 - six_3) / six_3)*10000)
        six_v2 = six_v1 / 10000
    three_six = three_v2 - six_v2
    three_six_1 = round(three_six * 100, 2)
    return three_six_1