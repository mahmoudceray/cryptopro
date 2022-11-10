import pandas as pd
import pandas_ta as ta
from warnings import simplefilter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


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
