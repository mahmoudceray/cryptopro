import talib

# حساب خط الدعم والمقاومة و اضافتها الى ملف موجود


def SupportResistance(df, senPP):

    ph1 = talib.MAX(df.High, senPP)
    pll = talib.MIN(df.Low, senPP)

    df['ph1'] = [ph1[i] if ph1[i] != 0 else ph1[i-1] for i in range(len(df))]
    df['pll'] = [pll[i] if pll[i] != 0 else pll[i-1] for i in range(len(df))]

    return df
