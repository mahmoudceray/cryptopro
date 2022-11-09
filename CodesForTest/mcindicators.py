import pandas as pd
import datetime
import os
import pandas_ta as ta
import math
import talib
import numpy as np
from binance import Client
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from warnings import simplefilter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

api_key = 'EH7SlsviwhlpiBLUY7MECXXuwgg1GW5sryau3AtYzgRKSbCJatNFV4513xHJlQCX'
api_secret = 'sY2VqMOsCDCDQOp029lwQUfWeKW0lutHzou2TYETHYTXSAfZoS2m5HDZwz1jrEcc'
bot_key = 'AAHJBZYe7XCCyc6wFBgyp2jxRp8tAwrFwDM'
chat_id = '929825457'
clinet = Client(api_key, api_secret)


def readdf(coin, interval, path):
    df = pd.read_csv('{}\\DataFromBinance{}\\{}{}.csv'.format(
        path, interval, coin, interval), header=[0])
    df = df.set_index('Open Time')
    df.index = pd.to_datetime(df.index)
    return df


def getdata(symbol, interval, lookback):
    df = pd.DataFrame(clinet.get_historical_klines(symbol, interval, lookback))
    df.columns = ["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time", "Quote asset volume",
                  "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"]
    df = df.astype(float)
    df = df.set_index('Open Time')
    df.index = pd.to_datetime(df.index, unit='ms')
    df.index = df.index + pd.Timedelta(hours=3)
    df.index
    return df

# من اجل جلب نص المسار الاساسي للملفات


def getPath():
    os.getcwd()
    os.chdir('../')
    os.chdir('../')
    return os.getcwd()

# تنزيل بيانات موجودة من بينانس و اضافتها الى ملف موجود


def getupdate(coins, intervals, path):
    coindata = pd.DataFrame()
    df = pd.DataFrame()
    df1 = pd.DataFrame()

    for coin in coins:
        for interval in intervals:
            df = pd.read_csv(r'D:\\OneDrive\\CryptoPro\\DataFromBinance{}\\{}{}.csv'.format(
                interval, coin, interval))

            StartTime = df.iloc[-2]["Open Time"]
            StartTime = datetime.datetime.strptime(
                StartTime, '%Y-%m-%d %H:%M:%S')
            StartTime = StartTime - pd.Timedelta(hours=3)
            StartTime = StartTime.strftime('%Y-%m-%d %H:%M:%S')

            coindata = getdata(coin, interval, StartTime)
            df = df.set_index('Open Time')
            df = df[:-2]
            df1 = pd.concat([df, coindata], axis=0)
            df1.to_csv(r'D:\\OneDrive\\CryptoPro\\DataFromBinance{}\\{}{}.csv'.format(
                interval, coin, interval))

            coindata = pd.DataFrame()
            df = pd.DataFrame()
            df1 = pd.DataFrame()

# حساب الحجوم و اضافتها الى ملف موجود


def getvolume(df):
    # BUYING VOLUME AND SELLING VOLUME

    BV = df.Volume * ((df.Close - df.Low) / (df.High - df.Low))
    SV = df.Volume * ((df.High - df.Close) / (df.High - df.Low))

    df["BVOLUME"] = BV
    df["SVOLUME"] = SV

    df["sell quote asset volume"] = df["Quote asset volume"] - \
        df["Taker buy quote asset volume"]

    df["net asset volume"] = df["Taker buy quote asset volume"] - \
        df["sell quote asset volume"]

    return df
# حساب مؤشرات البيع والشراء والمتوسطات و اضافتها الى ملف موجود


def getTAindic(df):
    df["ATR"] = ta.atr(df.High, df.Low, df.Close, length=8, mamode='wma')
    df["EMA"] = ta.ema(df.Close, length=55)
    df["RSI"] = ta.rsi(df.Close, length=5)
    df["VWMA"] = ta.vwma(df.Close, volume=df.Volume, length=13)
    df["RVI"] = ta.rvi(df.Close, df.High, df.Low, length=7, mamode='wma')
    df['MFI'] = ta.mfi(df.High, df.Low, df.Close, df.Volume, length=13)
    df['TR'] = ta.true_range(df.High, df.Low, df.Close)
    return df
# حساب مؤشرات تقنية و اضافتها الى ملف موجود


def getTAindic2(df):

    df = pd.concat([df, ta.supertrend(df.High, df.Low, df.Close,
                   length=8, multiplier=2.618, offset=0)], axis=1)

    df = pd.concat([df, ta.tsi(df.Close, fast=30, slow=8)], axis=1)

    df = pd.concat([df, ta.stoch(df.High, df.Low, df.Close,
                   k=13, d=8, smooth_k=3, mamode="wma")], axis=1)

    df = pd.concat([df, ta.stochrsi(df.High, length=21,
                   rsi_length=5, k=13, d=8, mamode="wma")], axis=1)

    df = pd.concat([df, ta.macd(df.Close, fast=8, slow=21, signal=5)], axis=1)

    df = pd.concat([df, ta.squeeze_pro(df.High, df.Low, df.Close, bb_length=13,
                   kc_length=13, mom_length=8, mom_smooth=3, tr=True, mamode="wma")], axis=1)
    return df

# حساب التجميع و التفريغ لوليام و اضافتها الى ملف موجود


def WilliamsAD(df):
    xWAD = []

    WAD = 0.0

    for i in range(len(df)):

        if df.Close.iloc[i] > df.Close.iloc[i-1]:
            WAD += df.Close.iloc[i] - df.Low.iloc[i-1]
            xWAD.append(WAD)

        elif df.Close.iloc[i] < df.Close.iloc[i-1]:
            WAD += df.Close.iloc[i] - df.High.iloc[i-1]
            xWAD.append(WAD)

        else:
            WAD = 0.0
            xWAD.append(WAD)

    df["xWAD"] = xWAD

    return df

# حساب التقلب و اضافتها الى ملف موجود


def volatility(df):
    Volatility = []
    r = []
    r_nor_p1 = 0
    len_short_term = 5
    len_long_term = 60
    Vola = pd.DataFrame()

    def rnor(so, len):
        s = (so - ta.wma(so, len)) / ta.stdev(so, len)
        s.astype(float)
        return s

    Vola['WMA_short_term'] = ta.wma(df.Close, len_short_term)

    for i in range(len(df)):
        z = abs(Vola['WMA_short_term'].iloc[i] - df['High'].iloc[i])
        y = abs(Vola['WMA_short_term'].iloc[i] - df['Low'].iloc[i])
        h = max(z, y)
        r.append(float(h))

    Vola["r"] = r  # مطابق للترند فيو

    Vola['r_nor'] = rnor(Vola.r, len_long_term)+1.1

    for i in range(len(Vola)):
        r_nor_p1 = (Vola['r_nor'].iloc[i]) if (
            Vola['r_nor'].iloc[i]) > 0.0 else 0.0
        Volatility.append(r_nor_p1)

    Vola["Volatility"] = Volatility
    df["Volatility"] = Volatility

# حساب و تحليل الفوليوم و اضافتها الى ملف موجود


def VSA(df):
    # ===================== Basic VSA Definitions =======================================
    df['volAvg'] = ta.sma(df.Volume, 40)
    df['volMean'] = ta.stdev(df.volAvg, 30)
    df['volUpBand3'] = df.volAvg + (3 * df.volMean)
    df['volUpBand2'] = df.volAvg + (2 * df.volMean)
    df['volUpBand1'] = df.volAvg + (1 * df.volMean)
    df['volDnBand1'] = df.volAvg - (1 * df.volMean)
    df['volDnBand2'] = df.volAvg - (2 * df.volMean)

    df['midprice'] = (df.High + df.Low) / 2
    df['spread'] = (df.High - df.Low)
    df['avgSpread'] = ta.sma(df.spread, 40)
    df['AvgSpreadBar'] = df.spread > df.avgSpread  # to be checked
    df['wideRangeBar'] = df.spread > (1.5 * df.avgSpread)
    df['narrowRangeBar'] = df.spread < (0.7 * df.avgSpread)

    df['lowVolume'] = [df.Volume[x] < df.Volume[x-1] and df.Volume[x] < df.Volume[x-2] and df.Volume[x] < df.volAvg[x]
                       if (df.Volume[x] < df.Volume[x-1] and df.Volume[x] < df.Volume[x-2] and df.Volume[x] < df.volAvg[x]) == True else False for x in range(len(df))]  # mods
    df['UpBar'] = df.Close > df.Close.shift(1)
    df['DownBar'] = df.Close < df.Close.shift(1)

    df['highVolume'] = [df.Volume[x] > df.Volume[x-1] and df.Volume[x-1] > df.Volume[x-2]
                        if ((df.Volume[x] > df.Volume[x-1]) and (df.Volume[x-1] > df.Volume[x-2])) == True else False for x in range(len(df))]  # Review
    df['closeFactor'] = df.Close - df.Low
    df['clsPosition'] = df.spread / df.closeFactor
    df['closePosition'] = [df.avgSpread[x] if df.closeFactor[x]
                           == 0 else df.clsPosition[x] for x in range(len(df))]

    df['vb'] = [df.Volume[x] > df.volAvg[x] or df.Volume[x] > df.Volume[x-1]
                for x in range(len(df))]
    # close is above 70% of the Bar
    df['upClose'] = df.Close >= ((df.spread * 0.7) + df.Low)
    # close is below the 30% of the bar
    df['downClose'] = df.Close <= ((df.spread * 0.3) + df.Low)
    # close is between 50% and 70% of the bar
    df['aboveClose'] = df.Close > ((df.spread * 0.5) + df.Low)
    # close is between 50% and 30% of the bar
    df['belowClose'] = df.Close < ((df.spread * 0.5) + df.Low)

    df['midClose'] = [(df.Close[x] > (df.spread[x] * 0.3) + df.Low[x]) and (df.Close[x] < (df.spread[x]
                                                                                           * 0.7) + df.Low[x]) for x in range(len(df))]  # close is between 30% and 70% of the bar
    df['veryLowClose'] = df.closePosition > 4  # close is below 25% of the bar
    # Close is above 80% of the bar
    df['veryHighClose'] = df.closePosition < 1.35

    df['iff_1'] = [4 if (df.Close[x] <= (df.spread[x] * 0.8) +
                         df.Low[x]) else 5 for x in range(len(df))]
    df['iff_2'] = [3 if (df.Close[x] <= (df.spread[x] * 0.6) +
                         df.Low[x]) else df.iff_1[x] for x in range(len(df))]
    df['iff_3'] = [2 if (df.Close[x] <= (df.spread[x] * 0.4) +
                         df.Low[x]) else df.iff_2[x] for x in range(len(df))]
    df['ClosePos'] = [1 if (df.Close[x] <= (
        df.spread[x] * 0.2) + df.Low[x]) else df.iff_3[x] for x in range(len(df))]

    # 1 = downClose, 2 = belowClose, 3 = midClose, 4 = aboveClose, 6 = upClose

    df['iff_4'] = [4 if ((df.Volume[x] < df.volAvg[x]) and (
        df.Volume[x] < (df.volAvg[x] * 0.7))) else 5 for x in range(len(df))]
    df['iff_5'] = [3 if (df.Volume[x] > df.volAvg[x])
                   else df.iff_4[x] for x in range(len(df))]
    df['iff_6'] = [2 if (df.Volume[x] > (df.volAvg[x] * 1.3))
                   else df.iff_5[x] for x in range(len(df))]
    df['volpos'] = [1 if (df.Volume[x] > (df.volAvg[x] * 2))
                    else df.iff_6[x] for x in range(len(df))]

    # 1 = veryhigh, 2 = High , 3 = AboveAverage, 4  = volAvg //LessthanAverage, 5 = lowVolume

    df['freshGndHi'] = [1 if (df.High[x] == max(df.High[x], df.High[x-5], df.High[x-4],
                              df.High[x-3], df.High[x-2], df.High[x-1])) else 0 for x in range(len(df))]
    df['freshGndLo'] = [1 if (df.Low[x] == min(df.Low[x], df.Low[x-5], df.Low[x-4],
                              df.Low[x-3], df.Low[x-2], df.Low[x-1])) else 0 for x in range(len(df))]

    # ---------------No Movement Bar--------------------
    df['pm'] = abs(df.Close - df.Open)  # price move
    df['pma'] = ta.sma(df.pm, 40)  # avg price move
    df['Lpm'] = df.pm < (0.5 * df.pma)  # small price move
    df['bw'] = [df.High[x] - df.Close[x] if df.Close[x] > df.Open[x]
                else df.High[x] - df.Open[x] for x in range(len(df))]  # wick
    df['bwh'] = df.bw >= (2 * df.pm)  # big wick

    df['fom1'] = [True if df.Volume[x] > (1.5 * df.volAvg[x]) and df.Lpm[x]
                  else False for x in range(len(df))]  # high volume not able to move the price

    # ---------------Two Bar Reversal  Dowm side--------------------
    df['tbcd'] = [(df.Close[x-1] < df.Close[x-5]) and (df.Close[x-1] < df.Close[x-4]) and (df.Close[x-1] < df.Close[x-3])
                  and (df.Close[x-1] < df.Close[x-2]) for x in range(len(df))]  # yesterday bar lower than last 4 bars

    df['tbc1'] = [(df.Low[x] < df.Low[x-1]) and (df.High[x] > df.High[x-1])
                  for x in range(len(df))]  # today bar shadoes yesterday bar

    df['tbc1a'] = [(df.Low[x] < df.Low[x-1]) and (df.Close[x]
                                                  > df.Close[x-1]) for x in range(len(df))]

    df['tbc2'] = [True if df.tbcd[x] == True and df.tbc1[x] == True and (df.Volume[x] > (
        1.2 * df.volAvg[x])) and df.upClose[x] == True else False for x in range(len(df))]

    df['tbc2a'] = [True if df.tbcd[x] == True and df.tbc1a[x] == True and (df.Volume[x] > (
        1.2 * df.volAvg[x])) and df.upClose[x] == True and df.tbc1[x] == False else False for x in range(len(df))]

    df['tbc3'] = [True if df.tbcd[x] == True and df.tbc1[x] == True and df.upClose[x] ==
                  True and (df.Volume[x] <= (1.2 * df.volAvg[x])) else False for x in range(len(df))]

    # ---------------- Two bar reversal Up side --------------------

    df['tbcu'] = [(df.Close[x-1] > df.Close[x-5]) and (df.Close[x-1] > df.Close[x-4]) and (
        df.Close[x-1] > df.Close[x-3]) and (df.Close[x-1] > df.Close[x-2]) for x in range(len(df))]

    df['tbc4'] = [True if df.tbcu[x] == True and df.tbc1[x] == True and df.Volume[x] > (
        1.2 * df.volAvg[x]) and df.downClose[x] == True else False for x in range(len(df))]

    df['tbc5'] = [True if df.tbcu[x] == True and df.tbc1[x] == True and df.downClose[x]
                  == True and df.Volume[x] <= (1.2 * df.volAvg[x]) else False for x in range(len(df))]

    # ====================Trend Analysis Module===============================

    psmin = 2  # Short term Min periods
    psmax = 8  # Short term Max Periods
    # ATR يستخدم فيه mamode="rma" افتراضي /// mamode='wma'  وانا افضل استخدام

    df['rshmin'] = (df.High - df.Low.shift(psmin)) / (ta.atr(df.High,
                                                             df.Low, df.Close, length=psmin) * math.sqrt(psmin))
    df['rshmax'] = (df.High - df.Low.shift(psmax)) / (ta.atr(df.High,
                                                             df.Low, df.Close, length=psmax) * math.sqrt(psmax))
    df['RWIHi'] = df[['rshmin', 'rshmax']].max(axis=1)

    # ATR يستخدم فيه mamode="rma" افتراضي /// mamode='wma'  وانا افضل استخدام
    df['rslmin'] = (df.High.shift(psmin) - df.Low) / (ta.atr(df.High,
                                                             df.Low, df.Close, length=psmin) * math.sqrt(psmin))
    df['rslmax'] = (df.High.shift(psmax) - df.Low) / (ta.atr(df.High,
                                                             df.Low, df.Close, length=psmax) * math.sqrt(psmax))
    df['RWILo'] = df[['rslmin', 'rslmax']].max(axis=1)

    df['k'] = df.RWIHi - df.RWILo
    df['ground'] = df.RWIHi
    df['sky'] = df.RWILo

    plmin = 10  # Long Term Min Periods
    plmax = 40  # Long term Max Periods

    # ATR يستخدم فيه mamode="rma" افتراضي /// mamode='wma'  وانا افضل استخدام
    df['rlhmin'] = (df.High - df.Low.shift(plmin)) / (ta.atr(df.High,
                                                             df.Low, df.Close, length=plmin) * math.sqrt(plmin))
    df['rlhmax'] = (df.High - df.Low.shift(plmax)) / (ta.atr(df.High,
                                                             df.Low, df.Close, length=plmax) * math.sqrt(plmax))
    df['RWILHi'] = df[['rlhmin', 'rlhmax']].max(axis=1)

    # ATR يستخدم فيه mamode="rma" افتراضي /// mamode='wma'  وانا افضل استخدام
    df['rllmin'] = (df.High.shift(plmin) - df.Low) / (ta.atr(df.High,
                                                             df.Low, df.Close, length=plmin) * math.sqrt(plmin))
    df['rllmax'] = (df.High.shift(plmax) - df.Low) / (ta.atr(df.High,
                                                             df.Low, df.Close, length=plmax) * math.sqrt(plmax))
    df['RWILLo'] = df[['rllmin', 'rllmax']].max(axis=1)

    df['j'] = (df.RWILHi - df.RWILLo).astype(float).fillna(0.0)
    df['j2'] = df.RWILHi.astype(float).fillna(0.0)
    df['k2'] = df.RWILLo.astype(float).fillna(0.0)

    dfone = pd.DataFrame(np.ones(len(df), dtype=int), columns=["One"])
    df_one = pd.DataFrame(
        np.full((len(df), 1), -1, dtype=int), columns=["_One"])

    df["One"] = dfone.One
    df['One'] = df['One'].fillna(1)

    df["_One"] = df_one._One
    df['_One'] = df['_One'].fillna(-1)

    # The following section check the diffeent condition of the RWi above and below zero
    # In oder to check which trend is doing what
    df['ja'] = [True if df.j[i] > df.One[i] and df.j[i-1]
                < df.One[i-1] else False for i in range(len(df))]
    df['jb'] = [True if df.One[i] > df.j[i] and df.One[i-1]
                < df.j[i-1] else False for i in range(len(df))]
    df['jc'] = [True if df._One[i] > df.j[i] and df._One[i-1]
                < df.j[i-1] else False for i in range(len(df))]
    df['jd'] = [True if df.j[i] > df._One[i] and df.j[i-1]
                < df._One[i-1] else False for i in range(len(df))]
    df['j2a'] = [True if df.j2[i] > df.One[i] and df.j2[i-1]
                 < df.One[i-1] else False for i in range(len(df))]
    df['j2b'] = [True if df.One[i] > df.j2[i] and df.One[i-1]
                 < df.j2[i-1] else False for i in range(len(df))]
    df['k2a'] = [True if df.k2[i] > df.One[i] and df.k2[i-1]
                 < df.One[i-1] else False for i in range(len(df))]
    df['k2b'] = [True if df.One[i] > df.k2[i] and df.One[i-1]
                 < df.k2[i-1] else False for i in range(len(df))]

    # Define the Major, Minor and Immediate trend Status

    df['upmajoron'] = [True if (
        df.j[i] > df.One[i]) and df.ja[i-1] == True else False for i in range(len(df))]

    df['upmajoroff'] = [True if (
        df.j[i] < df.One[i]) and df.jb[i-1] == True else False for i in range(len(df))]

    df['upminoron'] = [True if (
        df.j2[i] > df.One[i]) and df.j2a[i-1] == True else False for i in range(len(df))]

    df['upminoroff'] = [True if (
        df.j2[i] < df.One[i]) and df.j2b[i-1] == True else False for i in range(len(df))]

    df['dnmajoron'] = [True if (
        df.j[i] < df._One[i]) and df.jc[i-1] == True else False for i in range(len(df))]

    df['dnmajoroff'] = [True if (
        df.j[i] > df._One[i]) and df.jd[i-1] == True else False for i in range(len(df))]

    df['dnminoron'] = [True if (
        df.k2[i] > df.One[i]) and df.k2a[i-1] == True else False for i in range(len(df))]

    df['dnminoroff'] = [True if (
        df.k2[i] < df.One[i]) and df.k2b[i-1] == True else False for i in range(len(df))]

    df['upmid'] = [1 if (df.ground[i] > df.One[i])
                   else 0 for i in range(len(df))]

    df['dnimd'] = [1 if (df.sky[i] > df.One[i]) else 0 for i in range(len(df))]

    df['iff_7'] = [-1 if (df.j[i] < df._One[i]) else 0 for i in range(len(df))]

    df['upmajor'] = [1 if (df.j[i] > df.One[i]) else df.iff_7[i]
                     for i in range(len(df))]  # Major Trend

    df['upminor'] = [1 if (df.j2[i] > df.One[i]) else -
                     1 for i in range(len(df))]  # Minor Trend

    df['dnminor'] = [1 if (df.k2[i] > df.One[i]) else -
                     1 for i in range(len(df))]  # Mid Trend

    # ====================Slope Calculation ================================

    df['src'] = ta.vwma(df.Close, df.Volume)

    # -----------longterm trend---------------
    df['lts'] = ta.linreg(df.src, 45, 0)
    df['ltsprev'] = ta.linreg(df.Close.shift(3), 45, 0)
    df['ltsslope'] = ((df.lts - df.ltsprev) / 3)

    # -------------Medium Term Trend-------------
    df['mts'] = ta.linreg(df.src, 20, 0)
    df['mtsprev'] = ta.linreg(df.Close.shift(3), 20, 0)
    df['mtsslope'] = ((df.mts - df.mtsprev) / 3)

    # -------------short Term Trend-------------
    df['sts'] = ta.linreg(df.src, 13, 0)
    df['stsprev'] = ta.linreg(df.Close.shift(1), 3, 0)
    df['stsslope'] = ((df.sts - df.stsprev) / 2)
    df['tls'] = df.stsslope

    # -----------High longterm trend---------------
    df['Highlts'] = talib.LINEARREG(
        df.High, timeperiod=45) + (talib.LINEARREG(df.High, timeperiod=45) * 0.06)

    # -----------Low longterm trend---------------
    df['Lowlts'] = talib.LINEARREG(
        df.Low, timeperiod=45) - (talib.LINEARREG(df.Low, timeperiod=45) * 0.06)

    # =====================VSA SIGNAL GENERATION ================================

    df['MaxVolume'] = talib.MAX(df.Volume, timeperiod=60)

    # WRB and UHS in midterm trend
    df['upThrustBar'] = [True if df.wideRangeBar[i] and df.downClose[i] and (
        df.High[i] > df.High[i-1]) and df.upmid[i] == 1 else False for i in range(len(df))]

    # NEW SIGNAL - Upthrust after new short up move
    df['nut'] = [True if df.wideRangeBar[i] and df.downClose[i]
                 and df.freshGndHi[i] and df.highVolume[i] else False for i in range(len(df))]

    # Buying Climax
    df['bc'] = [True if df.wideRangeBar[i] and df.aboveClose[i] and df.upmajor[i]
                == 1 and df.MaxVolume[i] else False for i in range(len(df))]

    # after minor up trend
    df['upThrustBar1'] = [True if df.wideRangeBar[i] and (df.ClosePos[i] == 1 or df.ClosePos[i] == 2) and df.upminor[i] > 0 and df.High[i] > df.High[i-1] and (
        df.upmid[i] > 0 or df.upmajor[i] > 0) and (df.volpos[i] < 4) else False for i in range(len(df))]

    # occurs after a major uptrend
    df['upThrustBartrue'] = [True if df.wideRangeBar[i] and df.ClosePos[i] == 1 and df.upmajor[i]
                             > 0 and df.High[i] > df.High[i-1] and df.volpos[i] < 4 else False for i in range(len(df))]

    # The Bar after Upthrust Bar- Confirms weakness
    df['upThrustCond1'] = [True if df.upThrustBar[i-1] and df.DownBar[i]
                           and not df.narrowRangeBar[i] else False for i in range(len(df))]

    # The Bar after Upthrust Bar- Confirms weakness
    df['upThrustCond2'] = [True if df.upThrustBar[i-1] and df.DownBar[i]
                           and (df.Volume[i] > (df.volAvg[i] * 1.3)) else False for i in range(len(df))]

    # Review
    df['upThrustCond3'] = [True if df.upThrustBar[i] and (
        df.Volume[i] > (df.volAvg[i] * 2)) else False for i in range(len(df))]

    # Top Reversal bar
    df['highest10'] = talib.MAX(df.High, 10)
    df['topRevBar'] = [True if df.Volume[i-1] > df.volAvg[i] and df.UpBar[i-1] and df.wideRangeBar[i-1] and df.DownBar[i]
                       and df.downClose[i] and df.wideRangeBar[i] and df.upmajor[i] > 0 and df.High[i] == df.highest10[i] else False for i in range(len(df))]
    df['PseudoUpThrust'] = [True if df.UpBar[i-1] and df.High[i] > df.High[i-1] and df.Volume[i-1] >
                            (1.5 * df.volAvg[i]) and df.DownBar[i] and df.downClose[i] and not df.upThrustBar[i] else False for i in range(len(df))]
    df['pseudoUtCond'] = [True if df.PseudoUpThrust[i-1] and df.DownBar[i]
                          and df.downClose[i] and not df.upThrustBar[i] else False for i in range(len(df))]

    df['highest5'] = talib.MAX(df.High, 5)

    df['trendChange'] = [True if df.UpBar[i-1] and df.High[i] == df.highest5[i] and df.DownBar[i]
                         and (df.downClose[i] or df.midClose[i]) and df.Volume[i] > df.volAvg[i] and df.upmajor[i] > 0 and df.upmid[i] > 0 and not df.wideRangeBar[i] and not df.PseudoUpThrust[i] else False for i in range(len(df))]
    # in a up market
    df['noDemandBarUt'] = [True if df.UpBar[i] and df.narrowRangeBar[i] and df.lowVolume[i] and (df.aboveClose[i] or df.upClose[i]) and (
        df.upminor[i] >= 0 and df.upmid[i] >= 0 or df.upminor[i] <= 0 and df.upminor[i] >= 0) else False for i in range(len(df))]
    # in a down or sidewayss market
    df['noDemandBarDt'] = [True if df.UpBar[i] and df.narrowRangeBar[i] and df.lowVolume[i] and (
        df.aboveClose[i] or df.upClose[i]) and (df.upminor[i] <= 0 or df.upmid[i] <= 0) else False for i in range(len(df))]
    df['noSupplyBar'] = [True if df.DownBar[i] and df.narrowRangeBar[i]
                         and df.lowVolume[i] and df.midClose[i] else False for i in range(len(df))]

    df['lowest5'] = talib.MIN(df.Low, 5)

    df['lowVolTest'] = [True if df.Low[i] == df.lowest5[i] and df.upClose[i]
                        and df.lowVolume[i] else False for i in range(len(df))]
    df['lowVolTest1'] = [True if df.Low[i] == df.lowest5[i] and df.Volume[i] < df.volAvg[i] and df.Low[i] <
                         df.Low[i-1] and df.upClose[i] and df.upminor[i] > 0 and df.upmajor[i] > 0 else False for i in range(len(df))]
    df['lowVolTest2'] = [True if df.lowVolTest[i-1] and df.UpBar[i]
                         and df.upClose[i] else False for i in range(len(df))]

    # SellConditions

    df['sellCond1'] = [True if (df.upThrustCond1[i] or df.upThrustCond2[i]
                                or df.upThrustCond3[i]) else False for i in range(len(df))]
    df['sellCond2'] = [True if df.sellCond1[i-1]
                       == True else False for i in range(len(df))]
    df['sellCond'] = [True if df.sellCond1[i]
                      and df.sellCond2[i] else False for i in range(len(df))]

    # BuyConditions
    df['strengthDown0'] = [True if df.upmajor[i] < 0 and df.volpos[i] < 4 and df.DownBar[i-1] and df.UpBar[i]
                           and df.ClosePos[i] > 3 and df.upminor[i] < 0 and df.upmid[i] <= 0 else False for i in range(len(df))]
    # Strength after a down trend
    df['strengthDown'] = [True if df.volpos[i] < 4 and df.DownBar[i-1] and df.UpBar[i] and df.ClosePos[i]
                          > 3 and df.upmid[i] <= 00 and df.upminor[i] < 0 else False for i in range(len(df))]
    df['strengthDown1'] = [True if df.upmajor[i] < 0 and df.Volume[i] > (
        df.volAvg[i] * 1.5) and df.DownBar[i-1] and df.UpBar[i] and df.ClosePos[i] > 3 and df.upmid[i] <= 00 and df.upminor[i] < 0 else False for i in range(len(df))]
    df['strengthDown2'] = [True if df.upmid[i] <= 0 and df.Volume[i-1] < df.volAvg[i] and df.UpBar[i]
                           and df.veryHighClose[i] and df.volpos[i] < 4 else False for i in range(len(df))]
    df['buyCond1'] = [True if df.strengthDown[i]
                      or df.strengthDown1[i] else False for i in range(len(df))]
    df['buyCond'] = [True if df.UpBar[i] and df.buyCond1[i-1]
                     else False for i in range(len(df))]

    df['stopVolume'] = [True if df.Low[i] == df.lowest5[i] and (df.upClose[i] or df.midClose[i]) and df.Volume[i] > (
        1.5 * df.volAvg[i]) and df.upmajor[i] < 0 else False for i in range(len(df))]

    df['revUpThrust'] = [True if df.UpBar[i] and df.upClose[i] and df.Volume[i] > df.Volume[i-1] and df.Volume[i] > df.volAvg[i]
                         and df.wideRangeBar[i] and df.DownBar[i-1] and df.downClose[i-1] and df.upminor[i] < 0 else False for i in range(len(df))]

    df['effortUp'] = [True if (df.High[i] > df.High[i-1]) and (df.Low[i] > df.Low[i-1]) and (df.Close[i] > df.Close[i-1]) and (df.Close[i] >= (
        (df.High[i] - df.Low[i]) * 0.7) + df.Low[i]) and (df.spread[i] > df.avgSpread[i]) and (df.volpos[i] < 4) else False for i in range(len(df))]

    df['effortUpfail'] = [True if df.effortUp[i-1] and (df.upThrustBar[i] or df.upThrustCond1[i] or df.upThrustCond2[i]
                                                        or df.upThrustCond3[i] or (df.DownBar[i] and df.AvgSpreadBar[i])) else False for i in range(len(df))]

    df['effortDown'] = [True if (df.High[i] < df.High[i-1]) and (df.Low[i] < df.Low[i-1]) and (df.Close[i] < df.Close[i-1]) and (df.Close[i] <= (
        ((df.High[i] - df.Low[i]) * 0.25) + df.Low[i])) and df.wideRangeBar[i] and (df.Volume[i] > df.Volume[i-1]) else False for i in range(len(df))]

    df['effortDownFail'] = [True if df.effortDown[i-1]
                            and (df.UpBar[i] and df.AvgSpreadBar[i] or df.revUpThrust[i] or df.buyCond1[i]) else False for i in range(len(df))]

    df['upflag'] = [True if df.sellCond[i] or df.buyCond[i] or df.effortUp[i] or df.effortUpfail[i] or df.stopVolume[i] or df.effortDown[i] or df.effortDownFail[i] or df.revUpThrust[i]
                    or df.noDemandBarDt[i] or df.noDemandBarUt[i] or df.noSupplyBar[i] or df.lowVolTest[i] or df.lowVolTest1[i] or df.lowVolTest2[i] or df.bc[i] else False for i in range(len(df))]

    df['bullBar'] = [True if (df.Volume[i] > df.volAvg[i] or df.Volume[i] > df.Volume[i-1]) and df.Close[i] <= (
        df.spread[i] * 0.2) + df.Low[i] and df.UpBar[i] and not df.upflag[i] else False for i in range(len(df))]

    df['bearBar'] = [True if df.vb[i] and df.downClose[i] and df.DownBar[i] and df.spread[i]
                     > df.avgSpread[i] and not df.upflag[i] else False for i in range(len(df))]

    # NEW SIGNAL Selling Climax

    df['sc'] = [True if df.wideRangeBar[i] and df.belowClose[i] and df.Volume[i] ==
                df.MaxVolume[i] and df.upmajor[i] == -1 else False for i in range(len(df))]

    # =====================very important Signals========================

    #'Show Strength Signals (ST)' // 'Strength seen returning after a down trend.'

    df['EFD'] = df.effortDownFail
    df['ST1'] = df.strengthDown0
    df['ST2'] = [True if df.strengthDown[i]
                 and not df.strengthDown2[i] else False for i in range(len(df))]
    df['strcond'] = [True if df.strengthDown2[i] and not df.strengthDown0[i]
                     and not df.strengthDown[i] and not df.strengthDown1[i] else False for i in range(len(df))]
    df['ST3'] = df.strengthDown1
    df['ST4'] = [True if df.strengthDown2[i]
                 and df.strcond[i] else False for i in range(len(df))]
    df['ST5'] = [True if df.strengthDown2[i]
                 and not df.strcond[i] else False for i in range(len(df))]
    df['ST'] = [True if df.ST1[i] or df.ST2[i] or df.ST3[i]
                or df.ST4[i] or df.ST5[i] else False for i in range(len(df))]

    #'Show Up Thrusts (UT)' // 'An Upthrust Bar. A sign of weakness. High Volume adds weakness.  A down bar after Upthrust adds weakness'

    df['UT1'] = [True if df.upThrustBar[i] or df.upThrustBartrue[i]
                 else False for i in range(len(df))]
    df['UT2'] = [True if df.upThrustCond1[i]
                 or df.upThrustCond2[i] else False for i in range(len(df))]
    df['UT'] = [True if df.UT1[i] or df.UT2[i]
                else False for i in range(len(df))]

    #'Show Low Volume Supply Test (LVT/ST)'  //  'Test for supply. An upBar closing near High after a Test confirms strength.'

    df['lvt'] = [True if df.lowVolTest[i] or df.lowVolTest2[i]
                 else False for i in range(len(df))]

    return df

# حساب خط الدعم والمقاومة و اضافتها الى ملف موجود


def SupportResistance(df, senPP):

    ph1 = talib.MAX(df.High, senPP)
    pll = talib.MIN(df.Low, senPP)

    df['ph1'] = [ph1[i] if ph1[i] != 0 else ph1[i-1] for i in range(len(df))]
    df['pll'] = [pll[i] if pll[i] != 0 else pll[i-1] for i in range(len(df))]

    return df
# حساب الشمعات اليابانية و اضافتها الى ملف موجود


def candles(df):
    dfc = pd.DataFrame()

    # دوجيات
    dfc['rickshawman'] = df.ta.cdl_pattern(name="rickshawman")
    dfc['spinningtop'] = df.ta.cdl_pattern(name="spinningtop")
    dfc['shortline'] = df.ta.cdl_pattern(name="shortline")
    dfc['marubozu'] = df.ta.cdl_pattern(name="marubozu")
    dfc['longleggeddoji'] = df.ta.cdl_pattern(name="longleggeddoji")
    dfc['highwave'] = df.ta.cdl_pattern(name="highwave")
    dfc['gravestonedoji'] = df.ta.cdl_pattern(name="gravestonedoji")
    dfc['dragonflydoji'] = df.ta.cdl_pattern(name="dragonflydoji")
    dfc['dojistar'] = df.ta.cdl_pattern(name="dojistar")
    dfc['doji'] = df.ta.cdl_pattern(name="doji")
    dfc['closingmarubozu'] = df.ta.cdl_pattern(name="closingmarubozu")

    # نماذج ايجابية انعكاسية قوية

    # نماذج مميزة وقوية

    dfc['hammer'] = df.ta.cdl_pattern(name="hammer")
    dfc['piercing'] = df.ta.cdl_pattern(name="piercing")

    # نماذج ايجابية عادية

    dfc['invertedhammer'] = df.ta.cdl_pattern(name="invertedhammer")
    dfc['counterattack'] = df.ta.cdl_pattern(name="counterattack")
    dfc['homingpigeon'] = df.ta.cdl_pattern(name="homingpigeon")
    dfc['matchinglow'] = df.ta.cdl_pattern(name="matchinglow")
    dfc['morningdojistar'] = df.ta.cdl_pattern(name="morningdojistar")
    dfc['morningstar'] = df.ta.cdl_pattern(name="morningstar")
    dfc['unique3river'] = df.ta.cdl_pattern(name="unique3river")
    dfc['3inside'] = df.ta.cdl_pattern(name="3inside")
    dfc['3starsinsouth'] = df.ta.cdl_pattern(name="3starsinsouth")
    dfc['3whitesoldiers'] = df.ta.cdl_pattern(name="3whitesoldiers")
    dfc['sticksandwich'] = df.ta.cdl_pattern(name="sticksandwich")
    dfc['breakaway'] = df.ta.cdl_pattern(name="breakaway")
    dfc['concealbabyswall'] = df.ta.cdl_pattern(name="concealbabyswall")

    # نماذج سلبية انعكاسية قوية
    # نماذج مميزة وقوية

    dfc['hangingman'] = df.ta.cdl_pattern(name="hammer")
    dfc['darkcloudcover'] = df.ta.cdl_pattern(name="darkcloudcover")
    dfc['shootingstar'] = df.ta.cdl_pattern(name="shootingstar")
    dfc['3outside'] = df.ta.cdl_pattern(name="3outside")

    # نماذج سلبية عادية

    dfc['eveningdojistar'] = df.ta.cdl_pattern(name="eveningdojistar")
    dfc['eveningstar'] = df.ta.cdl_pattern(name="eveningstar")
    dfc['3blackcrows'] = df.ta.cdl_pattern(name="3blackcrows")
    dfc['identical3crows'] = df.ta.cdl_pattern(name="identical3crows")
    dfc['2crows'] = df.ta.cdl_pattern(name="2crows")
    dfc['upsidegap2crows'] = df.ta.cdl_pattern(name="upsidegap2crows")
    dfc['3inside'] = df.ta.cdl_pattern(name="3inside")
    dfc['advanceblock'] = df.ta.cdl_pattern(name="advanceblock")
    dfc['breakaway'] = df.ta.cdl_pattern(name="breakaway")
    dfc['stalledpattern'] = df.ta.cdl_pattern(name="stalledpattern")

    # نماذج مشتركة
    # قوية
    dfc['engulfing'] = df.ta.cdl_pattern(name="engulfing")
    dfc['kicking'] = df.ta.cdl_pattern(name="kicking")
    dfc['tristar'] = df.ta.cdl_pattern(name="tristar")
    dfc['3outside'] = df.ta.cdl_pattern(name="3outside")

    # عادية
    dfc['belthold'] = df.ta.cdl_pattern(name="belthold")
    dfc['harami'] = df.ta.cdl_pattern(name="harami")
    dfc['haramicross'] = df.ta.cdl_pattern(name="haramicross")
    dfc['abandonedbaby'] = df.ta.cdl_pattern(name="abandonedbaby")
    dfc['ladderbottom'] = df.ta.cdl_pattern(name="ladderbottom")
    dfc['hikkake'] = df.ta.cdl_pattern(name="hikkake")
    dfc['hikkakemod'] = df.ta.cdl_pattern(name="hikkakemod")

    dfc.fillna(0.0)

    dfc.replace({False: 0.0, True: 1.0}, inplace=True)
    dfc.replace({-100: -1.0, 100: 1.0}, inplace=True)
    dfc.replace({-200: -1.0, 200: 1.0}, inplace=True)

    df = pd.concat([df, dfc], axis=1)

    return df

# حساب التوقع الخطي و اضافتها الى ملف موجود


def LINEARREGCH(df, dev, shback):

    deviation = dev
    shiftback = shback

    # CLOSE Linear Regression

    df["slope"] = talib.LINEARREG_SLOPE(df.Close, timeperiod=shiftback)

    df["intercept"] = talib.LINEARREG_INTERCEPT(df.Close, timeperiod=shiftback)

    df["endy"] = df.intercept + df.slope * (shiftback-1)

    df["dev"] = talib.STDDEV(df.Close, timeperiod=shiftback, nbdev=1)

    # ======================================================================================

    df["y1RegCh0"] = df.intercept + df.dev * deviation * -1

    df["y2RegCh0"] = df.endy + df.dev * deviation * -1

    # ======================================================================================

    df["y1RegCh1"] = df.intercept + (df.dev * (deviation * 0))

    df["y2RegCh1"] = df.endy + (df.dev * (deviation * 0))

    # ======================================================================================

    df["y1RegCh2"] = df.intercept + (df.dev * (deviation * 1))

    df["y2RegCh2"] = df.endy + (df.dev * (deviation * 1))

    # =============================================================================
    # ======================================================================================
    # HIGH Linear Regression

    df["Hslope"] = talib.LINEARREG_SLOPE(df.High, timeperiod=shiftback)

    df["Hintercept"] = talib.LINEARREG_INTERCEPT(df.High, timeperiod=shiftback)

    df["Hendy"] = df.intercept + df.slope * (shiftback-1)

    df["Hdev"] = talib.STDDEV(df.High, timeperiod=shiftback, nbdev=1)

    df["Hy1RegCh1"] = df.Hintercept + (df.Hdev * (deviation * 1))

    df["Hy2RegCh1"] = df.Hendy + (df.Hdev * (deviation * 1))

    # ======================================================================================
    # Low Linear Regression

    df["Lslope"] = talib.LINEARREG_SLOPE(df.Low, timeperiod=shiftback)

    df["Lintercept"] = talib.LINEARREG_INTERCEPT(df.Low, timeperiod=shiftback)

    df["Lendy"] = df.intercept + df.slope * (shiftback-1)

    df["Ldev"] = talib.STDDEV(df.Low, timeperiod=shiftback, nbdev=1)

    df["Ly1RegCh1"] = df.Lintercept + (df.Ldev * (deviation * -1))

    df["Ly2RegCh1"] = df.Lendy + (df.Ldev * (deviation * -1))

    return df

# حساب خطوط المستويات و اضافتها الى ملف موجود


def levels(df):
    levels = [-110, -100, -90, -80, -70, -60, -50, -40, -30, -
              20, -10, 0, 2, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
    for x in levels:
        dfone = pd.DataFrame(np.ones(len(df), dtype=int),
                             columns=["{}".format(x)])
        df["{}".format(x)] = dfone["{}".format(x)]
        df["{}".format(x)] = df["{}".format(x)].fillna(x)


def WaveTrend(df, n1=8, n2=21):
    # Levels = 60 53 -60 -53
    df["ap"] = (df.High + df.Low + df.Close)/3
    df["esa"] = ta.wma(df.ap, n1)
    df["d"] = ta.wma(abs(df.ap - df.esa), n1)
    df["ci"] = (df.ap - df.esa) / (0.015 * df.d)
    df["tci"] = ta.wma(df.ci, n2)
    df["wt1"] = df.tci
    df["wt2"] = ta.wma(df.wt1, 4)

    return df


def WeisWaveVolume(df):

    dfC = pd.DataFrame()

    normalize = False

    isOscillating = True

    dfC['vol'] = ta.true_range(df.High, df.Low, df.Close)

    dfC['methodvalue'] = df.ATR

    currclose = [None, None, None, None, None, None, None]
    prevclose = [None, None, None, None, None, None, None]
    prevhigh = [None, None, None, None, None, None, None]
    prevlow = [None, None, None, None, None, None, None]

    for i in range(7, len(df)):
        if i == 7:
            currclose.append(df.Close[i-1])
            prevclose.append(currclose[i])
            prevhigh.append(currclose[i])
            prevlow.append(currclose[i])
            continue
        prevclose.append(currclose[i-1])
        prevhigh.append(prevclose[i] + dfC.methodvalue[i])
        prevlow.append(prevclose[i] - dfC.methodvalue[i])
        currclose.append(df.Close[i] if df.Close[i] > prevhigh[i]
                         or df.Close[i] < prevlow[i] else prevclose[i])

    dfC['currclose'] = currclose
    dfC['prevclose'] = prevclose
    dfC['prevhigh'] = prevhigh
    dfC['prevlow'] = prevlow

    # ============================================ to here it is ok

    direction = [None, None, None, None, None, None, None]

    for i in range(7, len(df)):
        if i == 7:
            direction.append(1)
            continue
        direction.append(1 if dfC.currclose[i] > dfC.prevclose[i] else -
                         1 if dfC.currclose[i] < dfC.prevclose[i] else direction[i-1])

    dfC['direction'] = direction

    dfC['directionHasChanged'] = [True if dfC.direction[i] !=
                                  dfC.direction[i-1] else False for i in range(len(df))]
    dfC['directionIsDown'] = [1 if dfC.direction[i]
                              < 0 else 0 for i in range(len(df))]

    barcount = [1, 1, 1, 1, 1, 1, 1]

    for i in range(7, len(df)):
        if i == 7:
            barcount.append(1)
            continue
        barcount.append(barcount[i-1] + barcount[i]
                        if not dfC.directionHasChanged[i] and normalize else barcount[i-1])

    dfC['barcount'] = barcount

    # =============================== it is ok
    vol = list(dfC['vol'])

    vol1 = [0, ]

    vol2 = 0

    for i in range(len(vol)):
        if not dfC.directionHasChanged[i]:
            vol2 = vol1[i] + dfC.vol[i]
            vol1.append(vol2)
        else:
            vol1.append(dfC.vol[i])

    dfC['vol1'] = vol1[1:]

    dfC['plotWWV'] = [-dfC.vol1[i] if isOscillating and dfC.directionIsDown[i]
                      == 1 else dfC.vol1[i] for i in range(len(df))]

    return dfC


def plotchart(df, FirstCandle, LastCandle, coin, time, colums=1, c=1, heights1=9, heights2=3):

    dfpl = df[FirstCandle: LastCandle]

    # first declare an empty figure
    fig = go.Figure()
    # Plot OHLC on 1st subplot (using the codes from before)

    fig = make_subplots(rows=16, cols=colums, shared_xaxes=False,
                        vertical_spacing=0.01,
                        row_heights=[heights1, heights1, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2])

    # add OHLC trace1 من حط لوب حتى نطالع شارتين تحت بعض
    fig.add_trace(go.Candlestick(x=dfpl.index,
                                 open=dfpl['Open'],
                                 high=dfpl['High'],
                                 low=dfpl['Low'],
                                 close=dfpl['Close'],
                                 showlegend=True,
                                 name="{} {}".format(coin, time)), row=1, col=c)

    # add ATR SUPERTREND trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['SUPERT_8_2.618'], line=dict(
        color='orange', width=1), name="ATR"), row=1, col=c)

    # add LINEAR REGRESSION  Long Trend trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.lts, line=dict(
        color='black', width=1), name="Long Trend"), row=1, col=c)

    # add LINEAR REGRESSION  Long Trend trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.Highlts, line=dict(
        color='red', width=2), name="High Long Trend"), row=1, col=c)

    # add LINEAR REGRESSION  Long Trend trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.Lowlts, line=dict(
        color='green', width=2), name="Low Long Trend"), row=1, col=c)

    # add Linear Regression Channel trace
    #line=dict(color='purple', width=1)

    fig.add_trace(go.Scatter(x=[dfpl.index[-150], dfpl.index[-1]], y=[
                  dfpl.y1RegCh2[-1], dfpl.y2RegCh2[-1]], mode="lines", name="RegChUp"), row=1, col=c)

    fig.add_trace(go.Scatter(x=[dfpl.index[-150], dfpl.index[-1]], y=[
                  dfpl.y1RegCh1[-1], dfpl.y2RegCh1[-1]], mode="lines", name="RegChMid"), row=1, col=c)

    fig.add_trace(go.Scatter(x=[dfpl.index[-150], dfpl.index[-1]], y=[
                  dfpl.y1RegCh0[-1], dfpl.y2RegCh0[-1]], mode="lines", name="RegChDown"), row=1, col=c)

    # add Support & Resistance Lines trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.ph1, line=dict(
        color='red', width=2), name="Support Line"), row=1, col=c)
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.pll, line=dict(
        color='blue', width=2), name="Resistance Line"), row=1, col=c)

    # end of OHLC trace1 ========================================================================================

    # add OHLC trace1 من حط لوب حتى نطالع شارتين تحت بعض
    fig.add_trace(go.Candlestick(x=dfpl.index,
                                 open=dfpl['Open'],
                                 high=dfpl['High'],
                                 low=dfpl['Low'],
                                 close=dfpl['Close'],
                                 showlegend=True,
                                 name="{} {}".format(coin, time)), row=2, col=c)

    fig.update_yaxes(title_text=f"{coin} {time}", row=2, col=c)

    # Plot Quote asset volume trace on 2th row
    #"cumsum net asset volume"
    #"net asset volume"
    netvolumecolors = ['green' if dfpl["net asset volume"]
                       [i] > 0 else 'red' for i in range(len(dfpl))]
    fig.add_trace(go.Bar(x=dfpl.index, y=dfpl["net asset volume"],
                  marker_color=netvolumecolors, showlegend=False), row=3, col=c)

    fig.update_yaxes(title_text="net asset volume", row=3, col=c)

    # Plot volume trace on 3nd row
    Volumecolors = ['green' if dfpl.Open[i] <
                    dfpl.Close[i] else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(
        x=dfpl.index, y=dfpl["Volume"], marker_color=Volumecolors, showlegend=False), row=4, col=c)

    fig.update_yaxes(title_text="Volume", row=4, col=c)

    # Plot Buy VOLUME trace on 4nd row
    fig.add_trace(go.Bar(
        x=dfpl.index, y=dfpl['BVOLUME'], marker_color='green', showlegend=False), row=5, col=c)
    fig.update_yaxes(title_text="B/S Volume", row=5, col=c)

    # Plot Sell volume trace on 4nd row
    fig.add_trace(go.Bar(
        x=dfpl.index, y=dfpl['SVOLUME'], marker_color='red', showlegend=False), row=5, col=c)
    fig.update_yaxes(title_text="B/S Volume", row=5, col=c)

    # Plot Volatility trace on 5nd row
    Volatilitycolors = ['green' if dfpl.Open[i] <
                        dfpl.Close[i] else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(x=dfpl.index, y=dfpl['Volatility'],
                  marker_color=Volatilitycolors, showlegend=False), row=6, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['2'],
                             line=dict(color='red', width=1), showlegend=False
                             ), row=6, col=c)

    fig.update_yaxes(title_text="Volatility", row=6, col=c)

    # Plot xWAD trace on 6nd row
    xWADcolors = ['green' if dfpl.xWAD[i] >=
                  0 else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl.xWAD,
                         marker_color=xWADcolors, showlegend=False
                         ), row=7, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['0'],
                             line=dict(color='red', width=1), showlegend=False
                             ), row=7, col=c)

    fig.update_yaxes(title_text="xWAD", row=7, col=c)

    # Plot MACD trace on 7rd row
    MACDhcolors = ['green' if dfpl.MACDh_8_21_5[i]
                   >= 0 else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl.MACDh_8_21_5,
                         marker_color=MACDhcolors,
                         showlegend=False
                         ), row=8, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.MACD_8_21_5,
                             line=dict(color='black', width=2),
                             showlegend=False
                             ), row=8, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.MACDs_8_21_5,
                             line=dict(color='blue', width=1),
                             showlegend=False
                             ), row=8, col=c)

    fig.update_yaxes(title_text="MACD", showgrid=False, row=8, col=c)

    # Plot TTMSqueeze trace on 8rd row
    TTMhcolors = ['green' if dfpl["SQZPRO_13_2.0_13_2_1.5_1"]
                  [i] >= 0 else 'red' for i in range(len(dfpl))]
    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl["SQZPRO_13_2.0_13_2_1.5_1"],
                         marker_color=TTMhcolors,
                         showlegend=False
                         ), row=9, col=c)

    fig.update_yaxes(title_text="TTMSqueeze", showgrid=False, row=9, col=c)

    # Plot stochastics trace on 9th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.STOCHRSIk_21_5_13_8,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=10, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.STOCHRSId_21_5_13_8,
                             line=dict(color='blue', width=1), showlegend=False
                             ), row=10, col=c)

    # Plot stochastics line levels trace on 9th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=10, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=10, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=10, col=c)

    fig.update_yaxes(title_text="STOCH RSI", row=10, col=c, range=[0, 100])

    # Plot TSI trace on 10th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.TSI_30_8_13,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.update_yaxes(title_text="TSI", row=11, col=c, range=[-70, 70])

    # Plot RSI trace on 11th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.RSI,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['40'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.update_yaxes(title_text=" RSI", row=12, col=c, range=[0, 100])

    # Plot RVI trace on 12th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.RVI,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['40'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.update_yaxes(title_text="RVI", row=13, col=c, range=[0, 100])

    # Plot MFI trace on 13th row
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.MFI, line=dict(
        color='black', width=2), showlegend=False), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['40'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.update_yaxes(title_text="MFI", row=14, col=c, range=[0, 100])

    # Plot WaveTrend trace on 14th row
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.wt1, line=dict(
        color='blue', width=2), showlegend=False), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.wt2, line=dict(
        color='red', width=2), showlegend=False), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['0'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.update_yaxes(title_text="WaveTrend", row=15, col=c, range=[-90, 90])

    # Plot WeisWaveVolume trace on 15rd row
    WeisWaveVolumeColor = ['green' if dfpl.plotWWV[i]
                           >= 0 else 'red' for i in range(len(dfpl))]
    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl.plotWWV,
                         marker_color=WeisWaveVolumeColor,
                         showlegend=False
                         ), row=16, col=c)

    fig.update_yaxes(title_text="Weis Wave Volume",
                     showgrid=False, row=16, col=c)

    fig.update_layout(
        autosize=True,
        width=7000,
        height=4000,
        xaxis_rangeslider_visible=False)

    fig.update_layout(xaxis1=dict(rangeslider=dict(visible=False)),
                      xaxis2=dict(rangeslider=dict(visible=False)),
                      xaxis3=dict(rangeslider=dict(visible=False)),
                      xaxis4=dict(rangeslider=dict(visible=False)),
                      xaxis5=dict(rangeslider=dict(visible=False)),
                      xaxis6=dict(rangeslider=dict(visible=False)),
                      xaxis7=dict(rangeslider=dict(visible=False)),
                      xaxis8=dict(rangeslider=dict(visible=False)),
                      xaxis9=dict(rangeslider=dict(visible=False)),
                      xaxis10=dict(rangeslider=dict(visible=False)),
                      xaxis11=dict(rangeslider=dict(visible=False)),
                      xaxis12=dict(rangeslider=dict(visible=False)),
                      xaxis13=dict(rangeslider=dict(visible=False)),
                      xaxis14=dict(rangeslider=dict(visible=False)),
                      xaxis15=dict(rangeslider=dict(visible=False)),
                      xaxis16=dict(rangeslider=dict(visible=False)),
                      yaxis1={'side': 'right'},
                      yaxis2={'side': 'right'},
                      yaxis3={'side': 'right'},
                      yaxis4={'side': 'right'},
                      yaxis5={'side': 'right'},
                      yaxis6={'side': 'right'},
                      yaxis7={'side': 'right'},
                      yaxis8={'side': 'right'},
                      yaxis9={'side': 'right'},
                      yaxis10={'side': 'right'},
                      yaxis11={'side': 'right'},
                      yaxis12={'side': 'right'},
                      yaxis13={'side': 'right'},
                      yaxis14={'side': 'right'},
                      yaxis15={'side': 'right'},
                      yaxis16={'side': 'right'},
                      )

    fig.show()


def everythings(df, coin, interval, TimeDeviation, colums=1, c=1, heights1=9, heights2=3):
    df = pd.DataFrame()
    df = readdf(coin, interval, 'D:\\OneDrive\\CryptoPro')
    df = df.drop(['Close Time', 'Number of trades', 'Ignore'], axis=1)
    df = getvolume(df)
    df = getTAindic(df)
    df = getTAindic2(df)
    df = WilliamsAD(df)
    df = pd.concat([df, volatility(df)], axis=1)
    df = VSA(df)
    df = SupportResistance(df, 55)
    df = candles(df)
    df = LINEARREGCH(df, dev=TimeDeviation, shback=130)
    df = WaveTrend(df, n1=8, n2=21)
    df = pd.concat([df, WeisWaveVolume(df)], axis=1)
    levels(df)
    plotchart(df, -750, -1, coin, time=interval,
              colums=colums, c=c, heights1=heights1, heights2=heights2)
    return df


def PlotCharts(df, FirstCandle, LastCandle, coin, time, colums=1, c=1, heights1=9, heights2=3):

    dfpl = df[FirstCandle: LastCandle]

    # first declare an empty figure
    # Plot OHLC on 1st subplot (using the codes from before)

    fig = make_subplots(rows=16, cols=colums, shared_xaxes=False,
                        vertical_spacing=0.01,
                        row_heights=[heights1, heights1, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2])

    # add OHLC trace1 من حط لوب حتى نطالع شارتين تحت بعض
    fig.add_trace(go.Candlestick(x=dfpl.index,
                                 open=dfpl['Open'],
                                 high=dfpl['High'],
                                 low=dfpl['Low'],
                                 close=dfpl['Close'],
                                 showlegend=True,
                                 name="{} {}".format(coin, time)), row=1, col=c)

    # add ATR SUPERTREND trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['SUPERT_8_2.618'], line=dict(
        color='orange', width=1), name="ATR"), row=1, col=c)

    # add LINEAR REGRESSION  Long Trend trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.lts, line=dict(
        color='black', width=1), name="Long Trend"), row=1, col=c)

    # add LINEAR REGRESSION  Long Trend trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.Highlts, line=dict(
        color='red', width=2), name="High Long Trend"), row=1, col=c)

    # add LINEAR REGRESSION  Long Trend trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.Lowlts, line=dict(
        color='green', width=2), name="Low Long Trend"), row=1, col=c)

    # add Linear Regression Channel trace
    #line=dict(color='purple', width=1)

    fig.add_trace(go.Scatter(x=[dfpl.index[-150], dfpl.index[-1]], y=[
                  dfpl.y1RegCh2[-1], dfpl.y2RegCh2[-1]], mode="lines", name="RegChUp"), row=1, col=c)

    fig.add_trace(go.Scatter(x=[dfpl.index[-150], dfpl.index[-1]], y=[
                  dfpl.y1RegCh1[-1], dfpl.y2RegCh1[-1]], mode="lines", name="RegChMid"), row=1, col=c)

    fig.add_trace(go.Scatter(x=[dfpl.index[-150], dfpl.index[-1]], y=[
                  dfpl.y1RegCh0[-1], dfpl.y2RegCh0[-1]], mode="lines", name="RegChDown"), row=1, col=c)

    # add Support & Resistance Lines trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.ph1, line=dict(
        color='red', width=2), name="Support Line"), row=1, col=c)
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.pll, line=dict(
        color='blue', width=2), name="Resistance Line"), row=1, col=c)

    # end of OHLC trace1 ========================================================================================

    # add OHLC trace1 من حط لوب حتى نطالع شارتين تحت بعض
    fig.add_trace(go.Candlestick(x=dfpl.index,
                                 open=dfpl['Open'],
                                 high=dfpl['High'],
                                 low=dfpl['Low'],
                                 close=dfpl['Close'],
                                 showlegend=True,
                                 name="{} {}".format(coin, time)), row=2, col=c)

    fig.update_yaxes(title_text=f"{coin} {time}", row=2, col=c)

    # Plot Quote asset volume trace on 2th row
    #"cumsum net asset volume"
    #"net asset volume"
    netvolumecolors = ['green' if dfpl["net asset volume"]
                       [i] > 0 else 'red' for i in range(len(dfpl))]
    fig.add_trace(go.Bar(x=dfpl.index, y=dfpl["net asset volume"],
                  marker_color=netvolumecolors, showlegend=False), row=3, col=c)

    fig.update_yaxes(title_text="net asset volume", row=3, col=c)

    # Plot volume trace on 3nd row
    Volumecolors = ['green' if dfpl.Open[i] <
                    dfpl.Close[i] else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(
        x=dfpl.index, y=dfpl["Volume"], marker_color=Volumecolors, showlegend=False), row=4, col=c)

    fig.update_yaxes(title_text="Volume", row=4, col=c)

    # Plot Buy VOLUME trace on 4nd row
    fig.add_trace(go.Bar(
        x=dfpl.index, y=dfpl['BVOLUME'], marker_color='green', showlegend=False), row=5, col=c)
    fig.update_yaxes(title_text="B/S Volume", row=5, col=c)

    # Plot Sell volume trace on 4nd row
    fig.add_trace(go.Bar(
        x=dfpl.index, y=dfpl['SVOLUME'], marker_color='red', showlegend=False), row=5, col=c)
    fig.update_yaxes(title_text="B/S Volume", row=5, col=c)

    # Plot Volatility trace on 5nd row
    Volatilitycolors = ['green' if dfpl.Open[i] <
                        dfpl.Close[i] else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(x=dfpl.index, y=dfpl['Volatility'],
                  marker_color=Volatilitycolors, showlegend=False), row=6, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['2'],
                             line=dict(color='red', width=1), showlegend=False
                             ), row=6, col=c)

    fig.update_yaxes(title_text="Volatility", row=6, col=c)

    # Plot xWAD trace on 6nd row
    xWADcolors = ['green' if dfpl.xWAD[i] >=
                  0 else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl.xWAD,
                         marker_color=xWADcolors, showlegend=False
                         ), row=7, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['0'],
                             line=dict(color='red', width=1), showlegend=False
                             ), row=7, col=c)

    fig.update_yaxes(title_text="xWAD", row=7, col=c)

    # Plot MACD trace on 7rd row
    MACDhcolors = ['green' if dfpl.MACDh_8_21_5[i]
                   >= 0 else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl.MACDh_8_21_5,
                         marker_color=MACDhcolors,
                         showlegend=False
                         ), row=8, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.MACD_8_21_5,
                             line=dict(color='black', width=2),
                             showlegend=False
                             ), row=8, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.MACDs_8_21_5,
                             line=dict(color='blue', width=1),
                             showlegend=False
                             ), row=8, col=c)

    fig.update_yaxes(title_text="MACD", showgrid=False, row=8, col=c)

    # Plot TTMSqueeze trace on 8rd row
    TTMhcolors = ['green' if dfpl["SQZPRO_13_2.0_13_2_1.5_1"]
                  [i] >= 0 else 'red' for i in range(len(dfpl))]
    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl["SQZPRO_13_2.0_13_2_1.5_1"],
                         marker_color=TTMhcolors,
                         showlegend=False
                         ), row=9, col=c)

    fig.update_yaxes(title_text="TTMSqueeze", showgrid=False, row=9, col=c)

    # Plot stochastics trace on 9th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.STOCHRSIk_21_5_13_8,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=10, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.STOCHRSId_21_5_13_8,
                             line=dict(color='blue', width=1), showlegend=False
                             ), row=10, col=c)

    # Plot stochastics line levels trace on 9th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=10, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=10, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=10, col=c)

    fig.update_yaxes(title_text="STOCH RSI", row=10, col=c, range=[0, 100])

    # Plot TSI trace on 10th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.TSI_30_8_13,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.update_yaxes(title_text="TSI", row=11, col=c, range=[-70, 70])

    # Plot RSI trace on 11th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.RSI,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['40'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.update_yaxes(title_text=" RSI", row=12, col=c, range=[0, 100])

    # Plot RVI trace on 12th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.RVI,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['40'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.update_yaxes(title_text="RVI", row=13, col=c, range=[0, 100])

    # Plot MFI trace on 13th row
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.MFI, line=dict(
        color='black', width=2), showlegend=False), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['40'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.update_yaxes(title_text="MFI", row=14, col=c, range=[0, 100])

    # Plot WaveTrend trace on 14th row
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.wt1, line=dict(
        color='blue', width=2), showlegend=False), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.wt2, line=dict(
        color='red', width=2), showlegend=False), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['0'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.update_yaxes(title_text="WaveTrend", row=15, col=c, range=[-90, 90])

    # Plot WeisWaveVolume trace on 15rd row
    WeisWaveVolumeColor = ['green' if dfpl.plotWWV[i]
                           >= 0 else 'red' for i in range(len(dfpl))]
    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl.plotWWV,
                         marker_color=WeisWaveVolumeColor,
                         showlegend=False
                         ), row=16, col=c)

    fig.update_yaxes(title_text="Weis Wave Volume",
                     showgrid=False, row=16, col=c)

    fig.update_layout(
        autosize=True,
        width=7000,
        height=4000,
        xaxis_rangeslider_visible=False)

    fig.update_layout(xaxis1=dict(rangeslider=dict(visible=False)),
                      xaxis2=dict(rangeslider=dict(visible=False)),
                      xaxis3=dict(rangeslider=dict(visible=False)),
                      xaxis4=dict(rangeslider=dict(visible=False)),
                      xaxis5=dict(rangeslider=dict(visible=False)),
                      xaxis6=dict(rangeslider=dict(visible=False)),
                      xaxis7=dict(rangeslider=dict(visible=False)),
                      xaxis8=dict(rangeslider=dict(visible=False)),
                      xaxis9=dict(rangeslider=dict(visible=False)),
                      xaxis10=dict(rangeslider=dict(visible=False)),
                      xaxis11=dict(rangeslider=dict(visible=False)),
                      xaxis12=dict(rangeslider=dict(visible=False)),
                      xaxis13=dict(rangeslider=dict(visible=False)),
                      xaxis14=dict(rangeslider=dict(visible=False)),
                      xaxis15=dict(rangeslider=dict(visible=False)),
                      xaxis16=dict(rangeslider=dict(visible=False)),
                      yaxis1={'side': 'right'},
                      yaxis2={'side': 'right'},
                      yaxis3={'side': 'right'},
                      yaxis4={'side': 'right'},
                      yaxis5={'side': 'right'},
                      yaxis6={'side': 'right'},
                      yaxis7={'side': 'right'},
                      yaxis8={'side': 'right'},
                      yaxis9={'side': 'right'},
                      yaxis10={'side': 'right'},
                      yaxis11={'side': 'right'},
                      yaxis12={'side': 'right'},
                      yaxis13={'side': 'right'},
                      yaxis14={'side': 'right'},
                      yaxis15={'side': 'right'},
                      yaxis16={'side': 'right'},
                      )
