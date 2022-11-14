import pandas as pd
import numpy as np
import pandas_ta as ta
from warnings import simplefilter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

# حساب الشمعات اليابانية و اضافتها الى ملف موجود


def pointpos(dfcc):
    for i in range(len(dfcc)):
        if dfcc == -1:
            return dfcc.Low-dfcc.ATR
        elif dfcc == 1:
            return dfcc.High+dfcc.ATR
        else:
            return np.nan


# تجربة هذه الطريقة باضافة الاشارات


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

    # حساب مواقع الشمعات

    # دوجيات
    dfc['rickshawmanPP'] = pointpos(dfc.rickshawman)
    dfc['spinningtopPP'] = pointpos(dfc.spinningtop)
    dfc['shortlinePP'] = pointpos(dfc.shortline)
    dfc['marubozuPP'] = pointpos(dfc.marubozu)
    dfc['longleggeddojiPP'] = pointpos(dfc.longleggeddoji)
    dfc['highwavePP'] = pointpos(dfc.highwave)
    dfc['gravestonedojiPP'] = pointpos(dfc.gravestonedoji)
    dfc['dragonflydojiPP'] = pointpos(dfc.dragonflydoji)
    dfc['dojistarPP'] = pointpos(dfc.dojistar)
    dfc['dojiPP'] = pointpos(dfc.doji)
    dfc['closingmarubozuPP'] = pointpos(dfc.closingmarubozu)

    # نماذج ايجابية انعكاسية قوية

    # نماذج مميزة وقوية

    dfc['hammerPP'] = pointpos(dfc.hammer)
    dfc['piercingPP'] = pointpos(dfc.piercing)

    # نماذج ايجابية عادية

    dfc['invertedhammerPP'] = pointpos(dfc.invertedhammer)
    dfc['counterattackPP'] = pointpos(dfc.counterattack)
    dfc['homingpigeonPP'] = pointpos(dfc.homingpigeon)
    dfc['matchinglowPP'] = pointpos(dfc.matchinglow)
    dfc['morningdojistarPP'] = pointpos(dfc.morningdojistar)
    dfc['morningstarPP'] = pointpos(dfc.morningstar)
    dfc['unique3riverPP'] = pointpos(dfc.unique3river)
    dfc['3insidePP'] = pointpos(dfc.3inside)
    dfc['3starsinsouthPP'] = pointpos(dfc.3starsinsouth)
    dfc['3whitesoldiersPP'] = pointpos(dfc.3whitesoldiers)
    dfc['sticksandwichPP'] = pointpos(dfc.sticksandwich)
    dfc['breakawayPP'] = pointpos(dfc.breakaway)
    dfc['concealbabyswallPP'] = pointpos(dfc.concealbabyswall)


    # نماذج سلبية انعكاسية قوية
    # نماذج مميزة وقوية

    dfc['hangingmanPP'] = pointpos(dfc.hammer)
    dfc['darkcloudcoverPP'] = pointpos(dfc.darkcloudcover)
    dfc['shootingstarPP'] = pointpos(dfc.shootingstar)
    dfc['3outsidePP'] = pointpos(dfc.3outside)

    # نماذج سلبية عادية

    dfc['eveningdojistarPP'] = pointpos(dfc.eveningdojistar)
    dfc['eveningstarPP'] = pointpos(dfc.eveningstar)
    dfc['3blackcrowsPP'] = pointpos(dfc.3blackcrows)
    dfc['identical3crowsPP'] = pointpos(dfc.identical3crows)
    dfc['2crowsPP'] = pointpos(dfc.2crows)
    dfc['upsidegap2crowsPP'] = pointpos(dfc.upsidegap2crows)
    dfc['3insidePP'] = pointpos(dfc.3inside)
    dfc['advanceblockPP'] = pointpos(dfc.advanceblock)
    dfc['breakawayPP'] = pointpos(dfc.breakaway)
    dfc['stalledpatternPP'] = pointpos(dfc.stalledpattern)

    # نماذج مشتركة
    # قوية
    dfc['engulfingPP'] = pointpos(dfc.engulfing)
    dfc['kickingPP'] = pointpos(dfc.kicking)
    dfc['tristarPP'] = pointpos(dfc.tristar)
    dfc['3outsidePP'] = pointpos(dfc.3outside)

    # عادية
    dfc['beltholdPP'] = pointpos(dfc.belthold)
    dfc['haramiPP'] = pointpos(dfc.harami)
    dfc['haramicrossPP'] = pointpos(dfc.haramicross)
    dfc['abandonedbabyPP'] = pointpos(dfc.abandonedbaby)
    dfc['ladderbottomPP'] = pointpos(dfc.ladderbottom)
    dfc['hikkakePP'] = pointpos(dfc.hikkake)
    dfc['hikkakemodPP'] = pointpos(dfc.hikkakemod)


    df = pd.concat([df, dfc], axis=1)

    return df
