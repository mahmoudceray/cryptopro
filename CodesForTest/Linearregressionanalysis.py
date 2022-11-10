import pandas as pd
import talib
import numpy as np
from warnings import simplefilter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

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
