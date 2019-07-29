import requests
import os
import pandas as pd
import numpy as np
import datetime
import logging

logging.basicConfig(filename="python.log", filemode='w', level=logging.DEBUG)


'''
用于成交明细分析的全局变量
'''
DETAIL_URL = 'http://quotes.money.163.com/cjmx/{0}/{1}/{2}.xls'
DETAIL_FOLDER = 'E:\\chaoduan\\details'
DETAIL_SESSION = requests.session()
DETAIL_RESULT = {}

'''
用于市净率计算的全局变量
'''
FINANCIAL_URL = 'http://quotes.money.163.com/service/zycwzb_{0}.html?type=report'
DAY_URL = 'http://quotes.money.163.com/service/chddata.html?code={0}&start=19901126&end={1}&fields=TCAP'
FINANCIAL_FOLDER = 'E:\\chaoduan\\financial'
FINANCIAL_SESSION = requests.session()
DAY_SESSION = requests.session()

'''
转化通达信日期为字符串
'''
def tr_date(tdx_date):
    _date = int(tdx_date)+ 19000000
    return str(_date)


def tr_code(tdx_code):
    code = int(tdx_code)
    return '%06d' % code


def add_prefix(code):
    if code[0] == '6':
        code = '0'+code
    else:
        code = '1'+code
    return code


def make_detail_url(code, date):
    year = date[0:4]
    code = add_prefix(code)
    return DETAIL_URL.format(year, date, code)


def make_financial_url(code):
    return FINANCIAL_URL.format(code)


def make_day_url(code):
    code = add_prefix(code)
    date = datetime.datetime.today()
    date = date.strftime('%Y%m%d')
    return DAY_URL.format(code, date)


def make_detail_xls_path(code, date):
    return os.path.join(DETAIL_FOLDER, date, code + '.csv')


def make_detail_date_folder(date):
    return os.path.join(DETAIL_FOLDER, date)


'''
通过传来的涨停类型去准备数据
0:未触及涨停
1:触及涨停
2：涨停收盘
对应dll 1号函数，应该首先被调用来准备数据
'''
def prepare(code, dates, zt_types):
    code = tr_code(code)
    for i in range(len(zt_types)):
        if zt_types[i] > 0:
            today = tr_date(dates[i])
            xls_path = make_detail_xls_path(code, today)
            if not os.path.exists(xls_path):
                date_folder = make_detail_date_folder(today)
                url = make_detail_url(code, today)
                with DETAIL_SESSION.get(url) as response:
                    if response.status_code == 200:
                        if not os.path.exists(date_folder):
                            os.mkdir(date_folder)
                        with open(xls_path, 'wb') as f:
                            f.write(response.content)
                        analyze_detail(code, today, zt_types[i])
            else:
                analyze_detail(code, today, zt_types[i])


def analyze_detail(code, date, zt_type):
    if code in DETAIL_RESULT and date in DETAIL_RESULT[code]:
        return
    if code not in DETAIL_RESULT:
        DETAIL_RESULT[code] = {}
    if date not in DETAIL_RESULT[code]:
        DETAIL_RESULT[code][date] = {}
    detail = pd.read_excel(make_detail_xls_path(code, date), dtype={'成交价':np.float, '成交量（手）':np.int})
    cjj = detail['成交价']
    cjsj = detail['成交时间']
    cjl = detail['成交量（手）']
    ztj = cjj.max()
# 计算首次上板时间
    scsb = None
    for index in detail.index:
        if cjj[index] == ztj:
            DETAIL_RESULT[code][date]['scsb'] = cjsj[index]
            scsb = index
            break
# 计算是否一次封死
    ycfs = 1
    for index in detail.index[scsb+1:]:
        if cjj[index] != ztj:
            ycfs = 0
            break
    DETAIL_RESULT[code][date]['ycfs'] = ycfs
# 计算首次开板时间
    if not ycfs:
        for index in detail.index[scsb+1:]:
            if cjj[index] != ztj:
                DETAIL_RESULT[code][date]['sckb'] = cjsj[index]
                break
    else:
        DETAIL_RESULT[code][date]['sckb'] = ''
# 计算最后一次回封时间
    if not ycfs and zt_type == 2:
        last = None
        for index in reversed(detail.index):
            if cjj[index] == ztj:
                last = index
                continue
            else:
                DETAIL_RESULT[code][date]['zhhf'] = cjsj[last]
                break
    else:
        DETAIL_RESULT[code][date]['zhhf'] = ''
# 统计高位成交量
# 我认为无需特别精确
    hp = (ztj / 1.1) * 1.07
    hp_vol = detail[cjj >= hp]['成交量（手）'].sum()
# 网易数据有时不准，直接计算占比避免bug
    DETAIL_RESULT[code][date]['gwcj'] = (hp_vol / cjl.sum()) * 100.0
    

# 对应dll二号函数
def get_scsb(outs, code, dates):
    code = tr_code(code)
    if code in DETAIL_RESULT:
        for i in range(len(dates)):
            today = tr_date(dates[i])
            if today in DETAIL_RESULT[code]:
                scsb = DETAIL_RESULT[code][today]['scsb']
                scsb = scsb.replace(':','')
                outs[i] = int(scsb)
            else:
                outs[i] = 0
    else:
        for i in range(len(dates)):
            outs[i] = 0


# 对应dll三号函数
def get_ycfs(outs, code, dates):
    code = tr_code(code)
    if code in DETAIL_RESULT:
        for i in range(len(dates)):
            today = tr_date(dates[i])
            if today in DETAIL_RESULT[code]:
                outs[i] = DETAIL_RESULT[code][today]['ycfs']
            else:
                outs[i] = -1
    else:
        for i in range(len(dates)):
            outs[i] = -1


# 对应dll四号函数
def get_sckb(outs, code, dates):
    code = tr_code(code)
    if code in DETAIL_RESULT:
        for i in range(len(dates)):
            today = tr_date(dates[i])
            if today in DETAIL_RESULT[code]:
                sckb = DETAIL_RESULT[code][today]['sckb']
                if sckb !='':
                    sckb = sckb.replace(':','')
                    outs[i] = int(sckb)
                else:
                    outs[i] = 0
            else:
                outs[i] = 0
    else:
        for i in range(len(dates)):
            outs[i] = 0    


# 对应dll五号函数
def get_zhhf(outs, code, dates):
    code = tr_code(code)
    if code in DETAIL_RESULT:
        for i in range(len(dates)):
            today = tr_date(dates[i])
            if today in DETAIL_RESULT[code]:
                zhhf = DETAIL_RESULT[code][today]['zhhf']
                if zhhf != '':
                    zhhf = zhhf.replace(':','')
                    outs[i] = int(zhhf)
                else:
                    outs[i] = 0
            else:
                outs[i] = 0
    else:
        for i in range(len(dates)):
            outs[i] = 0


# 对应dll六号函数
def get_gwcj(outs, code, dates):
    code = tr_code(code)
    if code in DETAIL_RESULT:
        for i in range(len(dates)):
            today = tr_date(dates[i])
            if today in DETAIL_RESULT[code]:
                gwcj = DETAIL_RESULT[code][today]['gwcj']
                outs[i] = gwcj
            else:
                outs[i] = 0
    else:
        for i in range(len(dates)):
            outs[i] = 0


# 对应dll七号函数
def get_lbcs(outs, code, dates, zt_types):
    for i in range(len(zt_types)):
        if i == 0:
            if zt_types[i] > 1:
                outs[0] = 1
            else:
                outs[0] = 0
        else:
            if zt_types[i] > 1:
                outs[i] = outs[i-1] + 1
            else:
                outs[i] = 0

# 对应dll八号函数
def get_jzc(outs, code, dates):
    key = '股东权益不含少数股东权益(万元)'
    code = tr_code(code)
    financial_url = make_financial_url(code)
    global FINANCIAL_SESSION
    if not FINANCIAL_SESSION.verify:
        FINANCIAL_SESSION = requests.session()
    with FINANCIAL_SESSION.get(financial_url) as response:
        if response.status_code == 200:
            path = os.path.join(FINANCIAL_FOLDER,'jzc.csv')
            with open(path, 'wb') as tmp:
                tmp.write(response.content)
            df = pd.read_csv(path, index_col=0, encoding='gbk')
            columns = df.columns[0:-1]
            for i in range(len(dates)-1,-1,-1):
                found = False
                date = tr_date(dates[i])
                for column in columns:
                    if df[column][key]=='--':
                        continue
                    target = column.replace('-', '')
                    if date >= target:
                        outs[i] = float(df[column][key])
                        found = True
                        break
                if not found:
                    outs[i] = float(df[columns[-1]][key])

# 对应dll九号函数
def get_sz(outs, code, dates, zfs):
    code = tr_code(code)
    day_url = make_day_url(code)
    global DAY_SESSION
    if not DAY_SESSION.verify:
        DAY_SESSION = requests.session()
    with DAY_SESSION.get(day_url) as response:
        if response.status_code == 200:
            path = os.path.join(FINANCIAL_FOLDER, 'shizhi.csv')
            with open(path, 'wb') as tmp:
                tmp.write(response.content)
            df = pd.read_csv(path, index_col=0, encoding='gbk')
            for i in range(len(dates)):
                date = tr_date(dates[i])
                date = date[0:4]+'-'+date[4:6]+'-'+date[6:8]
                zsz = df['总市值']
                if date in zsz.index:
                    outs[i] = zsz[date]
                else:
                    outs[i] = outs[i-1]+(zfs[i]/100.0)*outs[i-1]