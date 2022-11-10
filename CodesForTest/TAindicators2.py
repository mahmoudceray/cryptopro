import pandas as pd
import pandas_ta as ta
from warnings import simplefilter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

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
