import pandas as pd
import pandas_ta as ta
import math
import talib
import numpy as np
from warnings import simplefilter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

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

# حساب و تحليل الفوليوم و اضافتها الى ملف موجود


def pointpos(dfcc):
    for i in range(len(dfcc)):
        if dfcc == -1:
            return dfcc.Low-dfcc.ATR
        elif dfcc == 1:
            return dfcc.High+dfcc.ATR
        else:
            return np.nan


# تجربة هذه الطريقة باضافة الاشارات


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
