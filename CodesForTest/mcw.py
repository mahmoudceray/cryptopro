# %%
import pandas as pd
import numpy as np
import pandas_ta as ta
import plotly.graph_objects as go
import math
import talib
from datetime import datetime
from plotly.subplots import make_subplots
from backtesting import Strategy
from backtesting import Backtest
from warnings import simplefilter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

# %%
coin = "btc".upper()
time = "4h".upper()

# %%
#intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1mo']
intervals = ['1d', '4h', '1h', '15m', '5m']

# %%
coins = ['ADABTC', 'ADAUSDT', 'ADXBTC', 'ADXUSDT', 'AERGOBTC', 'AIONBTC', 'AIONUSDT', 'ALGOBTC', 'ALGOUSDT', 'ALICEBTC', 'ALICEUSDT',
        'ALPINEBTC', 'ALPINEUSDT', 'AMPBTC', 'ANKRBTC', 'ANKRUSDT', 'ANTBTC', 'ANTUSDT', 'API3BTC', 'API3USDT', 'ARBTC',
        'ARPABTC', 'ARPAUSDT', 'ARUSDT', 'ASRBTC', 'ASRUSDT', 'ATABTC', 'ATAUSDT', 'ATOMBTC', 'ATOMUSDT', 'AVABTC', 'AVAUSDT', 'AVAXBTC',
        'AVAXUSDT', 'AXSBTC', 'AXSUSDT', 'BALBTC', 'BALUSDT', 'BANDBTC', 'BANDUSDT', 'BATBTC', 'BATUSDT', 'BCHBTC', 'BCHUSDT', 'BEAMBTC',
        'BEAMUSDT', 'BLZBTC', 'BLZUSDT', 'BSWUSDT', 'BTCUSDT', 'BTTCUSDT', 'CELOBTC', 'CELOUSDT', 'CELRBTC', 'CELRUSDT', 'CFXBTC',
        'CFXUSDT', 'CHRBTC', 'CHRUSDT', 'CHZBTC', 'CHZUSDT', 'CKBUSDT', 'COCOSUSDT', 'COSBTC', 'COSUSDT', 'COTIBTC', 'COTIUSDT', 'CTKBTC',
        'CTKUSDT', 'CTSIBTC', 'CTSIUSDT', 'CTXCBTC', 'CTXCUSDT', 'CVCBTC', 'CVCUSDT', 'DASHBTC', 'DASHUSDT', 'DATABTC', 'DATAUSDT',
        'DCRBTC', 'DCRUSDT', 'DEGOBTC', 'DEGOUSDT', 'DENTUSDT', 'DGBBTC', 'DGBUSDT', 'DNTBTC', 'DNTUSDT', 'DOCKBTC', 'DOCKUSDT', 'DOGEBTC',
        'DOGEUSDT', 'DOTBTC', 'DOTUSDT', 'DREPBTC', 'DREPUSDT', 'DUSKBTC', 'DUSKUSDT', 'EGLDBTC', 'EGLDUSDT', 'ELFBTC', 'ELFUSDT', 'ENJBTC',
        'ENJUSDT', 'ENSBTC', 'ENSUSDT', 'EOSBTC', 'EOSUSDT', 'ETCBTC', 'ETCUSDT', 'ETHBTC', 'ETHUSDT', 'FETBTC', 'FETUSDT', 'FILBTC',
        'FILUSDT', 'FIOBTC', 'FIOUSDT', 'FIROBTC', 'FIROUSDT', 'FLOWBTC', 'FLOWUSDT', 'FLUXBTC', 'FTMBTC', 'FTMUSDT', 'FXSBTC', 'FXSUSDT',
        'GALABTC', 'GALAUSDT', 'GMTBTC', 'GRTBTC', 'GRTUSDT', 'GTCBTC', 'GTCUSDT', 'GTOBTC', 'GTOUSDT', 'HBARBTC', 'HBARUSDT', 'HIVEBTC',
        'HIVEUSDT', 'HNTBTC', 'HNTBUSD', 'HOTUSDT', 'ICPBTC', 'ICPUSDT', 'ICXBTC', 'ICXUSDT', 'IOSTBTC', 'IOSTUSDT', 'IOTABTC', 'IOTAUSDT',
        'IOTXBTC', 'IOTXUSDT', 'IRISBTC', 'IRISUSDT', 'JASMYBTC', 'JASMYUSDT', 'KDABTC', 'KDAUSDT', 'KEYUSDT', 'KLAYBTC', 'KLAYUSDT',
        'KMDBTC', 'KMDUSDT', 'KSMBTC', 'KSMUSDT', 'LINKBTC', 'LINKUSDT', 'LITBTC', 'LITUSDT', 'LOOMBTC', 'LRCBTC', 'LSKBTC', 'LSKUSDT',
        'LTCBTC', 'LTCUSDT', 'LTOBTC', 'LTOUSDT', 'MANABTC', 'MANAUSDT', 'MASKUSDT', 'MATICBTC', 'MATICUSDT', 'MBLUSDT', 'MCBTC', 'MCUSDT',
        'MDTBTC', 'MDTUSDT', 'MINABTC', 'MINAUSDT', 'MOBBTC', 'MOBUSDT', 'MTLBTC', 'MTLUSDT', 'MULTIBTC', 'MULTIUSDT', 'NEARBTC',
        'NEARUSDT', 'NEBLBTC', 'NKNBTC', 'NKNUSDT', 'NULSBTC', 'NULSUSDT', 'OCEANBTC', 'OCEANUSDT', 'OGNBTC', 'OGNUSDT', 'OMGBTC',
        'OMGUSDT', 'ONEBTC', 'ONEUSDT', 'ONGBTC', 'ONGUSDT', 'OPBTC', 'OPUSDT', 'ORNBTC', 'ORNUSDT', 'OXTBTC', 'OXTUSDT', 'PAXGBTC',
        'PAXGUSDT', 'PEOPLEBTC', 'PEOPLEUSDT', 'PERLBTC', 'PERLUSDT', 'PHABTC', 'PHAUSDT', 'PHBBTC', 'PIVXBTC', 'PNTBTC', 'PNTUSDT',
        'PONDBTC', 'PONDUSDT', 'POWRBTC', 'POWRUSDT', 'PROMBTC', 'PUNDIXUSDT', 'QLCBTC', 'QNTBTC', 'QNTUSDT', 'QTUMBTC', 'QTUMUSDT',
        'RADBTC', 'RADUSDT', 'REQBTC', 'REQUSDT', 'RIFBTC', 'RIFUSDT', 'RLCUSDT','RLCBTC', 'ROSEBTC', 'ROSEUSDT', 'RSRUSDT', 'RVNBTC', 'RVNUSDT',
        'SANDBTC', 'SANDUSDT', 'SCRTBTC', 'SCRTUSDT', 'SCUSDT', 'SFPBTC', 'SFPUSDT', 'SKLBTC', 'SKLUSDT', 'SOLBTC', 'SOLUSDT', 'STMXBTC',
        'STMXUSDT', 'STORJBTC', 'STORJUSDT', 'STRAXBTC', 'STRAXUSDT', 'STXBTC', 'STXUSDT', 'SXPBTC', 'SXPUSDT', 'SYSBTC', 'SYSUSDT',
        'TFUELBTC', 'TFUELUSDT', 'THETABTC', 'THETAUSDT', 'TOMOBTC', 'TOMOUSDT', 'TORNBTC', 'TORNUSDT', 'TRBBTC', 'TRBUSDT', 'TRXBTC',
        'TRXUSDT', 'TVKBTC', 'TVKUSDT', 'TWTBTC', 'TWTUSDT', 'UTKBTC', 'UTKUSDT', 'VETBTC', 'VETUSDT', 'VGXBTC', 'VGXUSDT', 'VIDTBTC',
        'VIDTUSDT', 'VTHOUSDT', 'WABIBTC', 'WAVESBTC', 'WAVESUSDT', 'WAXPBTC', 'WAXPUSDT', 'WTCBTC', 'WTCUSDT', 'XECUSDT', 'XEMBTC',
        'XEMUSDT', 'XLMBTC', 'XLMUSDT', 'XMRBTC', 'XMRUSDT', 'XNOBTC', 'XNOUSDT', 'XRPBTC', 'XRPUSDT', 'XTZBTC', 'XTZUSDT', 'ZECBTC',
        'ZECUSDT', 'ZENBTC', 'ZENUSDT', 'ZILBTC', 'ZILUSDT']

# %%
df = pd.DataFrame()
#df4h = pd.DataFrame()
#df1h = pd.DataFrame()
#df15m = pd.DataFrame()
#df5m = pd.DataFrame()

# %%
coins = ['BTC',]

# %%
for coin in coins:
    df = pd.read_csv(f'D:\\OneDrive\\CryptoPro\\DataFromBinance1d\\{coin}USDT1d.csv', header=[0])
    df = df.set_index('Open Time')
    df.index = pd.to_datetime(df.index)
    
    df4h = pd.read_csv(f'D:\\OneDrive\\CryptoPro\\DataFromBinance4h\\{coin}USDT4h.csv', header=[0])
    df4h = df4h.set_index('Open Time')
    df4h.index = pd.to_datetime(df4h.index)
    
    df1h = pd.read_csv(f'D:\\OneDrive\\CryptoPro\\DataFromBinance1h\\{coin}USDT1h.csv', header=[0])
    df1h = df1h.set_index('Open Time')
    df1h.index = pd.to_datetime(df1h.index)    
    
    df15m = pd.read_csv(f'D:\\OneDrive\\CryptoPro\\DataFromBinance15m\\{coin}USDT15m.csv', header=[0])
    df15m = df15m.set_index('Open Time')
    df15m.index = pd.to_datetime(df15m.index)     
    
    df5m = pd.read_csv(f'D:\\OneDrive\\CryptoPro\\DataFromBinance5m\\{coin}USDT5m.csv', header=[0])
    df5m = df5m.set_index('Open Time')
    df5m.index = pd.to_datetime(df5m.index)

# %%
df = pd.read_csv(f'D:\\OneDrive\\CryptoPro\\DataFromBinance{time}\\{coin}USDT{time}.csv', header=[0])
#df4h = pd.read_csv(f'D:\\OneDrive\\CryptoPro\\DataFromBinance{time}\\{coin}USDT{time}.csv', header=[0])
#df1h = pd.read_csv(f'D:\\OneDrive\\CryptoPro\\DataFromBinance{time}\\{coin}USDT{time}.csv', header=[0])
#df15m = pd.read_csv(f'D:\\OneDrive\\CryptoPro\\DataFromBinance{time}\\{coin}USDT{time}.csv', header=[0])
#df5m = pd.read_csv(f'D:\\OneDrive\\CryptoPro\\DataFromBinance{time}\\{coin}USDT{time}.csv', header=[0])
#df = pd.read_csv("FILUSDT-15m.csv")
#df = pd.read_csv("FILUSDT-30m.csv")

df = df.set_index('Open Time')
df.index = pd.to_datetime(df.index)

# %% [markdown]
# Buying Selling Volume 

# %%
#BUYING VOLUME AND SELLING VOLUME
BV = df.Volume * ((df.Close - df.Low) / (df.High - df.Low))
SV = df.Volume * ((df.High - df.Close) / (df.High - df.Low))

TP = BV + SV

df["BVOLUME"] = BV
df["SVOLUME"] = SV

# %%
df["sell quote asset volume"] = df["Quote asset volume"] - df["Taker buy quote asset volume"]

df["net asset volume"] = df["Taker buy quote asset volume"] - df["sell quote asset volume"]

#df["cumsum net asset volume"] = df["net asset volume"].cumsum(axis = 0)


# %% [markdown]
# #ATR مطابق لل تريدفيو

# %%
df["ATR"] = ta.atr(df.High, df.Low, df.Close, length=8, mamode='wma')

# %% [markdown]
# #Supertrend مطابق لل تريدفيو

# %%
Supertrend = ta.supertrend(df.High, df.Low, df.Close, length=8, multiplier=2.618, offset=0)

df = pd.concat([df, Supertrend["SUPERT_8_2.618"]], axis=1)

# %% [markdown]
# #TSI

# %%
df_tsi = ta.tsi(df['Close'], fast=30, slow=8)
df = pd.concat([df, df_tsi], axis=1)

# %% [markdown]
# #EMA مطابق لل تريدفيو

# %%
df["EMA"] = ta.ema(df.Close, length=55)

# %% [markdown]
# #RSI مطابق لل تريدفيو

# %%
df["RSI"] = ta.rsi(df.Close, length=5)

# %% [markdown]
# #VWMA مطابق لل تريدفيو

# %%
df["VWMA"] = ta.vwma(df.Close, volume=df.Volume , length=13)

# %% [markdown]
# #Relative Volatility Index  مطابق للترند فيو

# %%
df["RVI"] = ta.rvi(df.Close, df.High, df.Low, length=7, mamode='wma')

# %% [markdown]
# #Money Flow Index مطابق للترند فيو

# %%
df['MFI'] = ta.mfi(df.High, df.Low, df.Close, df.Volume, length=13)

# %% [markdown]
# #STOCH مطابق للترند فيو

# %%
df_stoch = ta.stoch(df.High, df.Low, df.Close, k=13, d=8, smooth_k=3, mamode="wma")

df = pd.concat([df, df_stoch], axis=1)

# %% [markdown]
# #STOCHRSI  مطابق للترند فيو

# %%
df_stochrsi = ta.stochrsi(df.High, length=21, rsi_length=5, k=13, d=8, mamode="wma")

df = pd.concat([df, df_stochrsi], axis=1)

# %% [markdown]
# #MACDمطابق للترند فيو 

# %%
df_macd = ta.macd(df.Close, fast=8, slow=21, signal=5)

df = pd.concat([df, df_macd], axis=1)

# %% [markdown]
# RAW Pressure Volume Calculations

# %%
BPV = (BV / TP) * df.Volume
SPV = (SV / TP) * df.Volume

TPV = BPV + SPV

# %% [markdown]
# Karthik Marar's Pressure Volume Normalized Version (XeL-MOD.)

# %%
VN = df.Volume / ta.ema(df.Volume, 20)
BPN = BV / (ta.wma(BV, 20) * VN * 100)
SPN = SV / (ta.wma(SV, 20) * VN * 100)
TPN = BPN + SPN


df["VN"] = VN
df["BPN"] = BPN
df["SPN"] = SPN
df["TPN"] = TPN

# %% [markdown]
# Conditional Selectors for RAW/Norm

# %%
BPc1 = BPV if BPV.all() > SPV.all() else abs(BPV)
BPc2 = BPN if BPN.all() > SPN.all() else abs(BPN)
SPc1 = SPV if SPV.all() > BPV.all() else abs(SPV)
SPc2 = SPN if SPN.all() > BPN.all() else abs(SPN)
BPcon = BPc2 if False else BPc1
SPcon = SPc2 if False else SPc1

# %% [markdown]
# #TTM Squeeze Pro مطابق للترند فيو

# %%
TTM = ta.squeeze_pro(df.High, df.Low, df.Close, bb_length=13, kc_length=13, mom_length=8, mom_smooth=3, tr=True, mamode="wma")

df["TTMSqueeze"] = TTM["SQZPRO_13_2.0_13_2_1.5_1"]

# %% [markdown]
# #Williams Accumulation/Distribution (Williams AD) مطابق للترند فيو 

# %%
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

# %% [markdown]
# #Volatility مطابق للترند فيو

# %%
Volatility = []
r = []
r_nor_p1 = 0
len_short_term = 5
len_long_term = 60
Vola = pd.DataFrame()

def rnor(so, len):
    s = (so - ta.wma(so, len) ) / ta.stdev(so, len)
    s.astype(float)
    return s
     
Vola['WMA_short_term'] = ta.wma(df.Close, len_short_term)

for i in range(len(df)):
    z = abs(Vola['WMA_short_term'].iloc[i] - df['High'].iloc[i])
    y = abs(Vola['WMA_short_term'].iloc[i] - df['Low'].iloc[i])
    h = max(z,y)
    r.append(float(h))

    
Vola["r"] = r #مطابق للترند فيو

Vola['r_nor'] = rnor(Vola.r, len_long_term)+1.1

for i in range(len(Vola)):
    r_nor_p1 = (Vola['r_nor'].iloc[i]) if (Vola['r_nor'].iloc[i]) > 0.0 else 0.0
    Volatility.append(r_nor_p1)

Vola["Volatility"] = Volatility
df["Volatility"] = Volatility

# %% [markdown]
# #================================================================VOLUME VSA Code

# %% [markdown]
# #===================== Basic VSA Definitions =======================================

# %%
df['volAvg'] = ta.sma(df.Volume, 40)
df['volMean'] = ta.stdev(df.volAvg, 30)
df['volUpBand3'] = df.volAvg + (3 * df.volMean)
df['volUpBand2'] = df.volAvg + (2 * df.volMean)
df['volUpBand1'] = df.volAvg + (1 * df.volMean)
df['volDnBand1'] = df.volAvg - (1 * df.volMean)
df['volDnBand2'] = df.volAvg - (2 * df.volMean)
#H = df.High
#L = df.Low
#V = df.Volume
#C = df.Close
#O = df.Open
df['midprice'] = (df.High + df.Low) / 2
df['spread'] = (df.High - df.Low)
df['avgSpread'] = ta.sma(df.spread, 40)
df['AvgSpreadBar'] = df.spread > df.avgSpread  #to be checked
df['wideRangeBar'] = df.spread > (1.5 * df.avgSpread)
df['narrowRangeBar'] = df.spread < (0.7 * df.avgSpread)

df['lowVolume'] = [df.Volume[x] < df.Volume[x-1] and df.Volume[x] < df.Volume[x-2] and df.Volume[x] < df.volAvg[x] \
if (df.Volume[x] < df.Volume[x-1] and df.Volume[x] < df.Volume[x-2] and df.Volume[x] < df.volAvg[x]) == True else False for x in range(len(df))] #mods
df['UpBar'] = df.Close > df.Close.shift(1)
df['DownBar'] = df.Close < df.Close.shift(1)

df['highVolume'] = [df.Volume[x] > df.Volume[x-1] and df.Volume[x-1] > df.Volume[x-2]\
if ((df.Volume[x] > df.Volume[x-1]) and (df.Volume[x-1] > df.Volume[x-2])) == True else False for x in range(len(df))] #Review
df['closeFactor'] = df.Close - df.Low
df['clsPosition'] = df.spread / df.closeFactor
df['closePosition'] = [df.avgSpread[x] if df.closeFactor[x] == 0 else df.clsPosition[x] for x in range(len(df))]

df['vb'] = [df.Volume[x] > df.volAvg[x] or df.Volume[x] > df.Volume[x-1] for x in range(len(df))]
df['upClose'] = df.Close >= ((df.spread * 0.7) + df.Low)  # close is above 70% of the Bar
df['downClose'] = df.Close <= ((df.spread * 0.3) + df.Low)  # close is below the 30% of the bar
df['aboveClose'] = df.Close > ((df.spread * 0.5) + df.Low)  # close is between 50% and 70% of the bar
df['belowClose'] = df.Close < ((df.spread * 0.5) + df.Low)  # close is between 50% and 30% of the bar

df['midClose'] = [(df.Close[x] > (df.spread[x] * 0.3) + df.Low[x]) and (df.Close[x] < (df.spread[x] * 0.7) + df.Low[x]) for x in range(len(df))] # close is between 30% and 70% of the bar
df['veryLowClose'] = df.closePosition > 4  #close is below 25% of the bar
df['veryHighClose'] = df.closePosition < 1.35  # Close is above 80% of the bar

df['iff_1'] = [4 if (df.Close[x] <= (df.spread[x] * 0.8) + df.Low[x]) else 5 for x in range(len(df))]
df['iff_2'] = [3 if (df.Close[x] <= (df.spread[x] * 0.6) + df.Low[x]) else df.iff_1[x] for x in range(len(df))]
df['iff_3'] = [2 if (df.Close[x] <= (df.spread[x] * 0.4) + df.Low[x]) else df.iff_2[x] for x in range(len(df))]
df['ClosePos'] = [1 if (df.Close[x] <= (df.spread[x] * 0.2) + df.Low[x]) else df.iff_3[x] for x in range(len(df))]

#1 = downClose, 2 = belowClose, 3 = midClose, 4 = aboveClose, 6 = upClose

df['iff_4'] = [4 if ((df.Volume[x] < df.volAvg[x]) and (df.Volume[x] < (df.volAvg[x] * 0.7))) else 5 for x in range(len(df))]
df['iff_5'] = [3 if (df.Volume[x] > df.volAvg[x]) else df.iff_4[x] for x in range(len(df))]
df['iff_6'] = [2 if (df.Volume[x] > (df.volAvg[x] * 1.3)) else df.iff_5[x] for x in range(len(df))]
df['volpos'] = [1 if (df.Volume[x] > (df.volAvg[x] * 2)) else df.iff_6[x] for x in range(len(df))]

#1 = veryhigh, 2 = High , 3 = AboveAverage, 4  = volAvg //LessthanAverage, 5 = lowVolume

df['freshGndHi'] = [1 if (df.High[x] == max(df.High[x], df.High[x-5], df.High[x-4], df.High[x-3], df.High[x-2], df.High[x-1])) else 0 for x in range(len(df))]
df['freshGndLo'] = [1 if (df.Low[x] == min(df.Low[x], df.Low[x-5], df.Low[x-4], df.Low[x-3], df.Low[x-2], df.Low[x-1])) else 0 for x in range(len(df))]

# %% [markdown]
# #---------------No Movement Bar--------------------

# %%

df['pm'] = abs(df.Close - df.Open)  #price move
df['pma'] = ta.sma(df.pm, 40)  #avg price move
df['Lpm'] = df.pm < (0.5 * df.pma)  #small price move
df['bw'] = [df.High[x] - df.Close[x] if df.Close[x] > df.Open[x] else df.High[x] - df.Open[x] for x in range(len(df))]  #wick
df['bwh'] = df.bw >= (2 * df.pm) #big wick

df['fom1'] = [True if df.Volume[x] > (1.5 * df.volAvg[x]) and df.Lpm[x] \
    else False for x in range(len(df))] #high volume not able to move the price


# %% [markdown]
# #---------------Two Bar Reversal  Dowm side--------------------

# %%
df['tbcd']  = [(df.Close[x-1] < df.Close[x-5]) and (df.Close[x-1] < df.Close[x-4]) and (df.Close[x-1] < df.Close[x-3]) and (df.Close[x-1] < df.Close[x-2]) for x in range(len(df))]  #yesterday bar lower than last 4 bars

df['tbc1']  = [(df.Low[x] < df.Low[x-1]) and (df.High[x] > df.High[x-1]) for x in range(len(df))]  # today bar shadoes yesterday bar

df['tbc1a'] = [(df.Low[x] < df.Low[x-1]) and (df.Close[x] > df.Close[x-1]) for x in range(len(df))]

df['tbc2']  = [True if df.tbcd[x] == True and df.tbc1[x] == True and (df.Volume[x] > (1.2 * df.volAvg[x])) and df.upClose[x] == True else False for x in range(len(df))]

df['tbc2a'] = [True if df.tbcd[x] == True and df.tbc1a[x] == True and (df.Volume[x] > (1.2 * df.volAvg[x])) and df.upClose[x] == True and df.tbc1[x] == False else False for x in range(len(df))]

df['tbc3']  = [True if df.tbcd[x] == True and df.tbc1[x] == True and df.upClose[x] == True and (df.Volume[x] <= (1.2 * df.volAvg[x])) else False for x in range(len(df))]


# %% [markdown]
# #---------------- Two bar reversal Up side --------------------

# %%
df['tbcu'] = [(df.Close[x-1] > df.Close[x-5]) and (df.Close[x-1] > df.Close[x-4]) and (df.Close[x-1] > df.Close[x-3]) and (df.Close[x-1] > df.Close[x-2]) for x in range(len(df))]

df['tbc4'] = [True if df.tbcu[x] == True and df.tbc1[x] == True and df.Volume[x] > (1.2 * df.volAvg[x]) and df.downClose[x] == True else False for x in range(len(df))]

df['tbc5'] = [True if df.tbcu[x] == True and df.tbc1[x] == True and df.downClose[x] == True  and df.Volume[x] <= (1.2 * df.volAvg[x]) else False for x in range(len(df))]

#الى هنا تمام ومطابق مع نريدفيو

# %% [markdown]
# #====================Trend Analysis Module===============================|
# 

# %%
psmin = 2 #Short term Min periods
psmax = 8 #Short term Max Periods
# ATR يستخدم فيه mamode="rma" افتراضي /// mamode='wma'  وانا افضل استخدام

df['rshmin'] = (df.High - df.Low.shift(psmin)) / (ta.atr(df.High, df.Low, df.Close, length=psmin) * math.sqrt(psmin))
df['rshmax'] = (df.High - df.Low.shift(psmax)) / (ta.atr(df.High, df.Low, df.Close, length=psmax) * math.sqrt(psmax))
df['RWIHi'] = df[['rshmin','rshmax']].max(axis=1)

# ATR يستخدم فيه mamode="rma" افتراضي /// mamode='wma'  وانا افضل استخدام
df['rslmin'] = (df.High.shift(psmin) - df.Low) / (ta.atr(df.High, df.Low, df.Close, length=psmin) * math.sqrt(psmin))
df['rslmax'] = (df.High.shift(psmax) - df.Low) / (ta.atr(df.High, df.Low, df.Close, length=psmax) * math.sqrt(psmax))
df['RWILo'] = df[['rslmin','rslmax']].max(axis=1)

df['k'] = df.RWIHi - df.RWILo
df['ground'] = df.RWIHi
df['sky'] = df.RWILo

plmin = 10 #Long Term Min Periods
plmax = 40 #Long term Max Periods

# ATR يستخدم فيه mamode="rma" افتراضي /// mamode='wma'  وانا افضل استخدام
df['rlhmin'] = (df.High - df.Low.shift(plmin)) / (ta.atr(df.High, df.Low, df.Close, length=plmin) * math.sqrt(plmin))
df['rlhmax'] = (df.High - df.Low.shift(plmax)) / (ta.atr(df.High, df.Low, df.Close, length=plmax) * math.sqrt(plmax))
df['RWILHi'] = df[['rlhmin','rlhmax']].max(axis=1)

# ATR يستخدم فيه mamode="rma" افتراضي /// mamode='wma'  وانا افضل استخدام
df['rllmin'] = (df.High.shift(plmin) - df.Low) / (ta.atr(df.High, df.Low, df.Close, length=plmin) * math.sqrt(plmin))
df['rllmax'] = (df.High.shift(plmax) - df.Low) / (ta.atr(df.High, df.Low, df.Close, length=plmax) * math.sqrt(plmax))
df['RWILLo'] = df[['rllmin','rllmax']].max(axis=1)

df['j'] = (df.RWILHi - df.RWILLo).astype(float).fillna(0.0)
df['j2'] = df.RWILHi.astype(float).fillna(0.0)
df['k2'] = df.RWILLo.astype(float).fillna(0.0)

# %%
dfone = pd.DataFrame(np.ones(len(df),dtype=int), columns=["One"])
df_one = pd.DataFrame(np.full((len(df), 1), -1, dtype=int), columns=["_One"])

df["One"] = dfone.One
df['One'] = df['One'].fillna(1)

df["_One"] = df_one._One
df['_One'] = df['_One'].fillna(-1)

# %%
# The following section check the diffeent condition of the RWi above and below zero
# In oder to check which trend is doing what
df['ja']  = [True if df.j[i] > df.One[i] and df.j[i-1] < df.One[i-1] else False for i in range(len(df))]
df['jb']  = [True if df.One[i] > df.j[i] and df.One[i-1] < df.j[i-1] else False for i in range(len(df))]
df['jc']  = [True if df._One[i] > df.j[i] and df._One[i-1] < df.j[i-1] else False for i in range(len(df))]
df['jd']  = [True if df.j[i] > df._One[i] and df.j[i-1] < df._One[i-1] else False for i in range(len(df))]
df['j2a'] = [True if df.j2[i] > df.One[i] and df.j2[i-1] < df.One[i-1] else False for i in range(len(df))]
df['j2b'] = [True if df.One[i] > df.j2[i] and df.One[i-1] < df.j2[i-1] else False for i in range(len(df))]
df['k2a'] = [True if df.k2[i] > df.One[i] and df.k2[i-1] < df.One[i-1] else False for i in range(len(df))]
df['k2b'] = [True if df.One[i] > df.k2[i] and df.One[i-1] < df.k2[i-1] else False for i in range(len(df))]


# %%
#Define the Major, Minor and Immediate trend Status

df['upmajoron'] = [True if (df.j[i] > df.One[i]) and df.ja[i-1] == True else False for i in range(len(df))]

df['upmajoroff'] = [True if (df.j[i] < df.One[i]) and df.jb[i-1] == True else False for i in range(len(df))]

df['upminoron'] = [True if (df.j2[i] > df.One[i]) and df.j2a[i-1] == True else False for i in range(len(df))]

df['upminoroff'] = [True if (df.j2[i] < df.One[i]) and df.j2b[i-1] == True else False for i in range(len(df))]

df['dnmajoron'] = [True if (df.j[i] < df._One[i]) and df.jc[i-1] == True else False for i in range(len(df))]

df['dnmajoroff'] = [True if (df.j[i] > df._One[i]) and df.jd[i-1] == True else False for i in range(len(df))]

df['dnminoron'] = [True if (df.k2[i] > df.One[i]) and df.k2a[i-1] == True else False for i in range(len(df))]

df['dnminoroff'] = [True if (df.k2[i] < df.One[i]) and df.k2b[i-1] == True else False for i in range(len(df))]

df['upmid'] = [1 if (df.ground[i] > df.One[i]) else 0 for i in range(len(df))]

df['dnimd'] = [1 if (df.sky[i] > df.One[i]) else 0 for i in range(len(df))]

df['iff_7'] = [-1 if (df.j[i] < df._One[i]) else 0 for i in range(len(df))]

df['upmajor'] = [1 if (df.j[i] > df.One[i]) else df.iff_7[i] for i in range(len(df))] #Major Trend

df['upminor'] = [1 if (df.j2[i] > df.One[i]) else -1 for i in range(len(df))]  #Minor Trend

df['dnminor'] = [1 if (df.k2[i] > df.One[i]) else -1 for i in range(len(df))]  #Mid Trend

# %% [markdown]
# #====================Slope Calculation ================================|

# %%
df['src'] = ta.vwma(df.Close, df.Volume)

#-----------longterm trend---------------
df['lts'] = ta.linreg(df.src, 45, 0)
df['ltsprev'] = ta.linreg(df.Close.shift(3), 45, 0)
df['ltsslope'] = ((df.lts - df.ltsprev) / 3)

#-------------Medium Term Trend-------------
df['mts'] = ta.linreg(df.src, 20, 0)
df['mtsprev'] = ta.linreg(df.Close.shift(3), 20, 0)
df['mtsslope'] = ((df.mts - df.mtsprev) / 3)

#-------------short Term Trend-------------
df['sts'] = ta.linreg(df.src, 13, 0)
df['stsprev'] = ta.linreg(df.Close.shift(1), 3, 0)
df['stsslope'] = ((df.sts - df.stsprev) / 2)
df['tls'] = df.stsslope

#-----------High longterm trend---------------
df['Highlts'] = talib.LINEARREG(df.High, timeperiod=45) + (talib.LINEARREG(df.High, timeperiod=45) * 0.06)


#-----------Low longterm trend---------------
df['Lowlts'] = talib.LINEARREG(df.Low, timeperiod=45) - (talib.LINEARREG(df.Low, timeperiod=45) * 0.06)


# %% [markdown]
# #=====================VSA SIGNAL GENERATION ================================|                

# %%
df['MaxVolume'] = talib.MAX(df.Volume, timeperiod=60)

# %%

#WRB and UHS in midterm trend
df['upThrustBar'] = [True if df.wideRangeBar[i] and df.downClose[i] and (df.High[i] > df.High[i-1]) and df.upmid[i] == 1 else False for i in range(len(df))]

# NEW SIGNAL - Upthrust after new short up move
df['nut'] = [True if df.wideRangeBar[i] and df.downClose[i] and df.freshGndHi[i] and df.highVolume[i] else False for i in range(len(df))]

# Buying Climax                           
df['bc'] = [True if df.wideRangeBar[i] and df.aboveClose[i] and df.upmajor[i] == 1 and df.MaxVolume[i] else False for i in range(len(df))]
   
# after minor up trend
df['upThrustBar1'] = [True if df.wideRangeBar[i] and (df.ClosePos[i] == 1 or df.ClosePos[i] == 2) and df.upminor[i] > 0 and df.High[i] > df.High[i-1] and (df.upmid[i] > 0 or df.upmajor[i] > 0) and (df.volpos[i] < 4) else False for i in range(len(df))]  

#occurs after a major uptrend
df['upThrustBartrue'] = [True if df.wideRangeBar[i] and df.ClosePos[i] == 1 and df.upmajor[i] > 0 and df.High[i] > df.High[i-1] and df.volpos[i] < 4 else False for i in range(len(df))]

# The Bar after Upthrust Bar- Confirms weakness
df['upThrustCond1'] = [True if df.upThrustBar[i-1] and df.DownBar[i] and not df.narrowRangeBar[i] else False for i in range(len(df))]

# The Bar after Upthrust Bar- Confirms weakness
df['upThrustCond2'] = [True if df.upThrustBar[i-1] and df.DownBar[i] and (df.Volume[i] > (df.volAvg[i] * 1.3)) else False for i in range(len(df))] 
 
# Review
df['upThrustCond3'] = [True if df.upThrustBar[i] and (df.Volume[i] > (df.volAvg[i] * 2)) else False for i in range(len(df))]  

# Top Reversal bar
df['highest10'] = talib.MAX(df.High, 10)
df['topRevBar'] = [True if df.Volume[i-1] > df.volAvg[i] and df.UpBar[i-1] and df.wideRangeBar[i-1] and df.DownBar[i] and df.downClose[i] and df.wideRangeBar[i] and df.upmajor[i] > 0 and df.High[i] == df.highest10[i] else False for i in range(len(df))]  
df['PseudoUpThrust'] = [True if df.UpBar[i-1] and df.High[i] > df.High[i-1] and df.Volume[i-1] > (1.5 * df.volAvg[i]) and df.DownBar[i] and df.downClose[i] and not df.upThrustBar[i] else False for i in range(len(df))]
df['pseudoUtCond'] = [True if df.PseudoUpThrust[i-1] and df.DownBar[i] and df.downClose[i] and not df.upThrustBar[i] else False for i in range(len(df))]

df['highest5'] = talib.MAX(df.High, 5)

df['trendChange'] = [True if df.UpBar[i-1] and df.High[i] == df.highest5[i] and df.DownBar[i] and (df.downClose[i] or df.midClose[i]) and df.Volume[i] > df.volAvg[i] and df.upmajor[i] > 0 and df.upmid[i] > 0 and not df.wideRangeBar[i] and not df.PseudoUpThrust[i] else False for i in range(len(df))]
#in a up market
df['noDemandBarUt'] = [True if df.UpBar[i] and df.narrowRangeBar[i] and df.lowVolume[i] and (df.aboveClose[i] or df.upClose[i]) and (df.upminor[i] >= 0 and df.upmid[i] >= 0 or df.upminor[i] <= 0 and df.upminor[i] >= 0) else False for i in range(len(df))]
 # in a down or sidewayss market  
df['noDemandBarDt'] = [True if df.UpBar[i] and df.narrowRangeBar[i] and df.lowVolume[i] and (df.aboveClose[i] or df.upClose[i]) and (df.upminor[i] <= 0 or df.upmid[i] <= 0) else False for i in range(len(df))]
df['noSupplyBar'] = [True if df.DownBar[i] and df.narrowRangeBar[i] and df.lowVolume[i] and df.midClose[i] else False for i in range(len(df))]

df['lowest5'] = talib.MIN(df.Low, 5)

df['lowVolTest'] = [True if df.Low[i] == df.lowest5[i] and df.upClose[i] and df.lowVolume[i] else False for i in range(len(df))]
df['lowVolTest1'] = [True if df.Low[i] == df.lowest5[i] and df.Volume[i] < df.volAvg[i] and df.Low[i] < df.Low[i-1] and df.upClose[i] and df.upminor[i] > 0 and df.upmajor[i] > 0 else False for i in range(len(df))]
df['lowVolTest2'] = [True if df.lowVolTest[i-1] and df.UpBar[i] and df.upClose[i] else False for i in range(len(df))]

#SellConditions

df['sellCond1'] = [True if (df.upThrustCond1[i] or df.upThrustCond2[i] or df.upThrustCond3[i]) else False for i in range(len(df))]
df['sellCond2'] = [True if df.sellCond1[i-1] == True else False for i in range(len(df))]
df['sellCond'] = [True if df.sellCond1[i] and df.sellCond2[i] else False for i in range(len(df))]

#BuyConditions
df['strengthDown0'] = [True if df.upmajor[i] < 0 and df.volpos[i] < 4 and df.DownBar[i-1] and df.UpBar[i] and df.ClosePos[i] > 3 and df.upminor[i] < 0 and df.upmid[i] <= 0 else False for i in range(len(df))]
# Strength after a down trend
df['strengthDown'] = [True if df.volpos[i] < 4 and df.DownBar[i-1] and df.UpBar[i] and df.ClosePos[i] > 3 and df.upmid[i] <= 00 and df.upminor[i] < 0 else False for i in range(len(df))]
df['strengthDown1'] = [True if df.upmajor[i] < 0 and df.Volume[i] > (df.volAvg[i] * 1.5) and df.DownBar[i-1] and df.UpBar[i] and df.ClosePos[i] > 3 and df.upmid[i] <= 00 and df.upminor[i] < 0 else False for i in range(len(df))]
df['strengthDown2'] = [True if df.upmid[i] <= 0 and df.Volume[i-1] < df.volAvg[i] and df.UpBar[i] and df.veryHighClose[i] and df.volpos[i] < 4 else False for i in range(len(df))]
df['buyCond1'] = [True if df.strengthDown[i] or df.strengthDown1[i] else False for i in range(len(df))]
df['buyCond'] = [True if df.UpBar[i] and df.buyCond1[i-1] else False for i in range(len(df))]

df['stopVolume'] = [True if df.Low[i] == df.lowest5[i] and (df.upClose[i] or df.midClose[i]) and df.Volume[i] > (1.5 * df.volAvg[i]) and df.upmajor[i] < 0 else False for i in range(len(df))]

df['revUpThrust'] = [True if df.UpBar[i] and df.upClose[i] and df.Volume[i] > df.Volume[i-1] and df.Volume[i] > df.volAvg[i] and df.wideRangeBar[i] and df.DownBar[i-1] and df.downClose[i-1] and df.upminor[i] < 0 else False for i in range(len(df))]

df['effortUp'] = [True if (df.High[i] > df.High[i-1]) and (df.Low[i] > df.Low[i-1]) and (df.Close[i] > df.Close[i-1]) and (df.Close[i] >= ((df.High[i] - df.Low[i]) * 0.7) + df.Low[i]) and (df.spread[i] > df.avgSpread[i]) and (df.volpos[i] < 4) else False for i in range(len(df))]

df['effortUpfail'] = [True if df.effortUp[i-1] and (df.upThrustBar[i] or df.upThrustCond1[i] or df.upThrustCond2[i] or df.upThrustCond3[i] or (df.DownBar[i] and df.AvgSpreadBar[i])) else False for i in range(len(df))]

df['effortDown'] = [True if (df.High[i] < df.High[i-1]) and (df.Low[i] < df.Low[i-1]) and (df.Close[i] < df.Close[i-1]) and (df.Close[i] <= (((df.High[i] - df.Low[i]) * 0.25) + df.Low[i])) and df.wideRangeBar[i] and (df.Volume[i] > df.Volume[i-1]) else False for i in range(len(df))]

df['effortDownFail'] = [True if df.effortDown[i-1] and (df.UpBar[i] and df.AvgSpreadBar[i] or df.revUpThrust[i] or df.buyCond1[i]) else False for i in range(len(df))]

df['upflag'] = [True if df.sellCond[i] or df.buyCond[i] or df.effortUp[i] or df.effortUpfail[i] or df.stopVolume[i] or df.effortDown[i] or df.effortDownFail[i] or df.revUpThrust[i] or df.noDemandBarDt[i] or df.noDemandBarUt[i] or df.noSupplyBar[i] or df.lowVolTest[i] or df.lowVolTest1[i] or df.lowVolTest2[i] or df.bc[i] else False for i in range(len(df))]

df['bullBar'] = [True if (df.Volume[i] > df.volAvg[i] or df.Volume[i] > df.Volume[i-1]) and df.Close[i] <= (df.spread[i] * 0.2) + df.Low[i] and df.UpBar[i] and not df.upflag[i] else False for i in range(len(df))]

df['bearBar'] = [True if df.vb[i] and df.downClose[i] and df.DownBar[i] and df.spread[i] > df.avgSpread[i] and not df.upflag[i] else False for i in range(len(df))]

# NEW SIGNAL Selling Climax

df['sc'] = [True if df.wideRangeBar[i] and df.belowClose[i] and df.Volume[i] == df.MaxVolume[i] and df.upmajor[i] == -1 else False for i in range(len(df))]  



# %% [markdown]
# #=========================================/very important Signals/===============================================

# %%
#'Show Strength Signals (ST)' // 'Strength seen returning after a down trend.'

df['EFD'] = df.effortDownFail
df['ST1'] = df.strengthDown0
df['ST2'] = [True if df.strengthDown[i] and not df.strengthDown2[i] else False for i in range(len(df))]
df['strcond'] =[True if df.strengthDown2[i] and not df.strengthDown0[i] and not df.strengthDown[i] and not df.strengthDown1[i] else False for i in range(len(df))]
df['ST3'] = df.strengthDown1
df['ST4'] = [True if df.strengthDown2[i] and df.strcond[i] else False for i in range(len(df))]
df['ST5'] = [True if df.strengthDown2[i] and not df.strcond[i] else False for i in range(len(df))]
df['ST'] = [True if df.ST1[i] or df.ST2[i] or df.ST3[i] or df.ST4[i] or df.ST5[i] else False for i in range(len(df))]


#'Show Up Thrusts (UT)' // 'An Upthrust Bar. A sign of weakness. High Volume adds weakness.  A down bar after Upthrust adds weakness'

df['UT1'] = [True if df.upThrustBar[i] or df.upThrustBartrue[i] else False for i in range(len(df))]
df['UT2'] = [True if df.upThrustCond1[i] or df.upThrustCond2[i] else False for i in range(len(df))]
df['UT'] = [True if df.UT1[i] or df.UT2[i] else False for i in range(len(df))]


#'Show Low Volume Supply Test (LVT/ST)'  //  'Test for supply. An upBar closing near High after a Test confirms strength.'

df['lvt'] = [True if df.lowVolTest[i] or df.lowVolTest2[i] else False for i in range(len(df))]


#الى هنا تمام ومطابق مع نريدفيو 

# %% [markdown]
# //========================Support & Resistance Lines================================|

# %%
sens = 55

ph1 = talib.MAX(df.High, sens)
pll = talib.MIN(df.Low, sens)

df['ph1']  = [ph1[i] if ph1[i] != 0 else ph1[i-1] for i in range(len(df))]
df['pll'] = [pll[i] if pll[i] != 0 else pll[i-1] for i in range(len(df))]

#الى هنا تمام ومطابق مع نريدفيو 

# %% [markdown]
# Candle Patterns

# %%
# Get all candle patterns (This is the default behaviour)
#dfcandles = df.ta.cdl_pattern(name="all")


# %%
dfc = pd.DataFrame()


#دوجيات
dfc['rickshawman'] = df.ta.cdl_pattern(name="rickshawman")
dfc['spinningtop'] = df.ta.cdl_pattern(name="spinningtop")
dfc['shortline'] = df.ta.cdl_pattern(name="shortline")
dfc['marubozu'] = df.ta.cdl_pattern(name="marubozu")
dfc['longleggeddoji'] = df.ta.cdl_pattern(name="longleggeddoji")
dfc['highwave'] = df.ta.cdl_pattern(name="highwave")
dfc['gravestonedoji'] = df.ta.cdl_pattern(name="gravestonedoji")
dfc['dragonflydoji'] = df.ta.cdl_pattern(name="dragonflydoji")
dfc['dojistar'] = df.ta.cdl_pattern(name="dojistar")#
dfc['doji'] = df.ta.cdl_pattern(name="doji")#
dfc['closingmarubozu'] = df.ta.cdl_pattern(name="closingmarubozu")#



#نماذج ايجابية انعكاسية قوية

#نماذج مميزة وقوية

dfc['hammer'] = df.ta.cdl_pattern(name="hammer")
dfc['piercing'] = df.ta.cdl_pattern(name="piercing")

#نماذج ايجابية عادية

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



#نماذج سلبية انعكاسية قوية
#نماذج مميزة وقوية

dfc['hangingman'] = df.ta.cdl_pattern(name="hammer")
dfc['darkcloudcover'] = df.ta.cdl_pattern(name="darkcloudcover")
dfc['shootingstar'] = df.ta.cdl_pattern(name="shootingstar")
dfc['3outside'] = df.ta.cdl_pattern(name="3outside")

#نماذج سلبية عادية

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



#نماذج مشتركة
#قوية
dfc['engulfing'] = df.ta.cdl_pattern(name="engulfing")#
dfc['kicking'] = df.ta.cdl_pattern(name="kicking")#
dfc['tristar'] = df.ta.cdl_pattern(name="tristar")#
dfc['3outside'] = df.ta.cdl_pattern(name="3outside")#

#عادية
dfc['belthold'] = df.ta.cdl_pattern(name="belthold")#
dfc['harami'] = df.ta.cdl_pattern(name="harami")#
dfc['haramicross'] = df.ta.cdl_pattern(name="haramicross")#
dfc['abandonedbaby'] = df.ta.cdl_pattern(name="abandonedbaby")#
dfc['ladderbottom'] = df.ta.cdl_pattern(name="ladderbottom")#
dfc['hikkake'] = df.ta.cdl_pattern(name="hikkake")#
dfc['hikkakemod'] = df.ta.cdl_pattern(name="hikkakemod")#


# %%
dfc.replace({False: 0.0, True: 1.0}, inplace=True)

# %%
dfc.replace({-100: -1.0, 100: 1.0}, inplace=True)

# %%
dfc.replace({-200: -1.0, 200: 1.0}, inplace=True)

# %%
df = pd.concat([df, dfc], axis=1)

# %%
#adding levels 50
levels = [-110,-100,-90, -80,-70, -60, -50,-40, -30, -20,-10, 0 ,2 , 10, 20, 30,40, 50, 60,70, 80 ,90,100,110]
for x in levels:
    dfone = pd.DataFrame(np.ones(len(df),dtype=int), columns=["{}".format(x)])
    df["{}".format(x)] = dfone["{}".format(x)]
    df["{}".format(x)] = df["{}".format(x)].fillna(x)


# %% [markdown]
# CLOSE Linear Regression Channel

# %%
deviation = 1.8

shiftback = 250

#CLOSE Linear Regression

df["slope"] = talib.LINEARREG_SLOPE(df.Close, timeperiod=shiftback)

df["intercept"] = talib.LINEARREG_INTERCEPT(df.Close, timeperiod=shiftback)

df["endy"] = df.intercept + df.slope * (shiftback-1)

df["dev"] = talib.STDDEV(df.Close, timeperiod=shiftback, nbdev= 1)


#======================================================================================
#HIGH Linear Regression


df["Hslope"] = talib.LINEARREG_SLOPE(df.High, timeperiod=shiftback)

df["Hintercept"] = talib.LINEARREG_INTERCEPT(df.High, timeperiod=shiftback)

df["Hendy"] = df.intercept + df.slope * (shiftback-1)

df["Hdev"] = talib.STDDEV(df.High, timeperiod=shiftback, nbdev= 1)


#======================================================================================
#Low Linear Regression


df["Lslope"] = talib.LINEARREG_SLOPE(df.Low, timeperiod=shiftback)

df["Lintercept"] = talib.LINEARREG_INTERCEPT(df.Low, timeperiod=shiftback)

df["Lendy"] = df.intercept + df.slope * (shiftback-1)

df["Ldev"] = talib.STDDEV(df.Low, timeperiod=shiftback, nbdev= 1)



#======================================================================================

df["y1RegCh0"] = df.intercept + df.dev * deviation * -1

df["y2RegCh0"] = df.endy + df.dev * deviation * -1

#======================================================================================

df["y1RegCh1"] = df.intercept + (df.dev * (deviation * 0))

df["y2RegCh1"] = df.endy + (df.dev * (deviation * 0))

#======================================================================================

df["y1RegCh2"] = df.intercept + (df.dev * (deviation * 1))

df["y2RegCh2"] = df.endy + (df.dev * (deviation * 1))

#======================================================================================
#======================================================================================

df["Ly1RegCh1"] = df.Lintercept + (df.Ldev * (deviation * -1))

df["Ly2RegCh1"] = df.Lendy + (df.Ldev * (deviation * -1))

#======================================================================================

df["Hy1RegCh1"] = df.Hintercept + (df.Hdev * (deviation * 1))

df["Hy2RegCh1"] = df.Hendy + (df.Hdev * (deviation * 1))


# %%
#WaveTrend
n1=8
n2=21
    # Levels = 60 53 -60 -53
df["ap"] = (df.High + df.Low + df.Close)/3
df["esa"] = ta.wma(df.ap, n1)
df["d"] = ta.wma(abs(df.ap - df.esa), n1)
df["ci"] = (df.ap - df.esa) / (0.015 * df.d)
df["tci"] = ta.wma(df.ci, n2)
df["wt1"] = df.tci
df["wt2"] = ta.wma(df.wt1, 4)

# %%
#WeisWaveVolume

normalize = False

isOscillating = True

methodvalue = 8.0

df['vol'] = ta.true_range(df.High, df.Low, df.Close)

df['methodvalue'] = df.ATR

# %%
currclose = [None,None,None,None,None,None,None]
prevclose = [None,None,None,None,None,None,None]
prevhigh = [None,None,None,None,None,None,None]
prevlow = [None,None,None,None,None,None,None]

for i in range(7,len(df)):
    if i == 7:
        currclose.append(df.Close[i-1])
        prevclose.append(currclose[i])
        prevhigh.append(currclose[i])
        prevlow.append(currclose[i])
        continue
    prevclose.append(currclose[i-1])
    prevhigh.append(prevclose[i] + df.methodvalue[i])
    prevlow.append(prevclose[i] - df.methodvalue[i])
    currclose.append(df.Close[i] if df.Close[i] > prevhigh[i] or df.Close[i] < prevlow[i] else prevclose[i])

df['currclose'] = currclose
df['prevclose'] = prevclose
df['prevhigh'] = prevhigh
df['prevlow'] = prevlow

# ============================================ to here it is ok

# %%
direction=[None,None,None,None,None,None,None]

for i in range(7,len(df)):
    if i == 7:
        direction.append(1)
        continue
    direction.append(1 if df.currclose[i] > df.prevclose[i] else -1 if df.currclose[i] < df.prevclose[i] else direction[i-1])

df['direction'] = direction


df['directionHasChanged'] = [ True if df.direction[i] != df.direction[i-1] else False for i in range(len(df))]
df['directionIsDown'] = [ 1 if df.direction[i] < 0 else 0 for i in range(len(df))]


barcount=[1,1,1,1,1,1,1]

for i in range(7,len(df)):
    if i == 7:
        barcount.append(1)
        continue
    barcount.append(barcount[i-1] + barcount[i] if not df.directionHasChanged[i] and normalize else barcount[i-1])
    
df['barcount'] = barcount

#=============================== it is ok
vol = list(df['vol'])

vol1 = [0,]

vol2 = 0

for i in range(len(vol)):
    if not df.directionHasChanged[i]:
        vol2 = vol1[i] + df.vol[i]
        vol1.append(vol2)
    else:
        vol1.append(df.vol[i])

df['vol1'] = vol1[1:]

df['plotWWV'] = [ -df.vol1[i] if isOscillating and df.directionIsDown[i] == 1 else df.vol1[i] for i in range(len(df))]

# %% [markdown]
# #Plot Candlestick Chart

# %%
dfpl = df[-700:]

# first declare an empty figure
fig = go.Figure()

heights1 = 9

heights2 = 2.5

# Plot OHLC on 1st subplot (using the codes from before)
#for i in range(1,6):
    
fig = make_subplots(rows=16, cols=1, shared_xaxes=False,
                    vertical_spacing=0.01, 
                    row_heights=[heights1, heights1, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2])
    
# add OHLC trace1 من حط لوب حتى نطالع شارتين تحت بعض
fig.add_trace(go.Candlestick(x=dfpl.index,
                             open=dfpl['Open'],
                             high=dfpl['High'],
                             low=dfpl['Low'],
                             close=dfpl['Close'], 
                             showlegend=True,
                             name="{} {}".format(coin, time)))


# add ATR SUPERTREND trace
fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['SUPERT_8_2.618'], line=dict(color='orange', width=1), name="ATR"))

# add LINEAR REGRESSION  Long Trend trace
fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.lts, line=dict(color='black', width=1), name="Long Trend"))

# add LINEAR REGRESSION  Long Trend trace
fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.Highlts, line=dict(color='red', width=2), name="High Long Trend"))

# add LINEAR REGRESSION  Long Trend trace
fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.Lowlts, line=dict(color='green', width=2), name="Low Long Trend"))


# add Linear Regression Channel trace
#line=dict(color='purple', width=1)

fig.add_trace(go.Scatter(x=[dfpl.index[-250],dfpl.index[-1]] , y=[dfpl.y1RegCh2[-1], dfpl.y2RegCh2[-1]], mode="lines",name="RegChUp"))

fig.add_trace(go.Scatter(x=[dfpl.index[-250],dfpl.index[-1]] , y=[dfpl.y1RegCh1[-1], dfpl.y2RegCh1[-1]], mode="lines",name="RegChMid"))

fig.add_trace(go.Scatter(x=[dfpl.index[-250],dfpl.index[-1]] , y=[dfpl.y1RegCh0[-1], dfpl.y2RegCh0[-1]], mode="lines",name="RegChDown"))


# add Support & Resistance Lines trace
fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.ph1, line=dict(color='red', width=2), name="Support Line"))
fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.pll, line=dict(color='blue', width=2), name="Resistance Line"))

# end of OHLC trace1 ========================================================================================

# add OHLC trace1 من حط لوب حتى نطالع شارتين تحت بعض
fig.add_trace(go.Candlestick(x=dfpl.index,
                             open=dfpl['Open'],
                             high=dfpl['High'],
                             low=dfpl['Low'],
                             close=dfpl['Close'], 
                             showlegend=True,
                             name="{} {}".format(coin, time)), row=2, col=1)

fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.doji + dfpl.High, mode="markers"), row=2, col=1)

fig.update_yaxes(title_text=f"{coin} {time}", row=2, col=1)


# end of OHLC trace2 ========================================================================================




# Plot Quote asset volume trace on 2th row
#"cumsum net asset volume"
#"net asset volume"
netvolumecolors = ['green' if dfpl["net asset volume"][i] > 0 else 'red' for i in range(len(dfpl))]
fig.add_trace(go.Bar(x=dfpl.index, y=dfpl["net asset volume"], marker_color= netvolumecolors ,showlegend=False), row=3, col=1)

fig.update_yaxes(title_text="net asset volume", row=3, col=1)


# Plot volume trace on 3nd row 
Volumecolors = ['green' if dfpl.Open[i] < dfpl.Close[i] else 'red' for i in range(len(dfpl))]

fig.add_trace(go.Bar(x=dfpl.index, y=dfpl["Volume"], marker_color=Volumecolors, showlegend=False), row=4, col=1)

fig.update_yaxes(title_text="Volume", row=4, col=1)


# Plot Buy VOLUME trace on 4nd row 
fig.add_trace(go.Bar(x=dfpl.index, y=dfpl['BVOLUME'], marker_color='green', showlegend=False), row=5, col=1)
fig.update_yaxes(title_text="B/S Volume", row=5, col=1)

# Plot Sell volume trace on 4nd row 
fig.add_trace(go.Bar(x=dfpl.index, y=dfpl['SVOLUME'], marker_color='red', showlegend=False), row=5, col=1)
fig.update_yaxes(title_text="B/S Volume", row=5, col=1)



# Plot Volatility trace on 5nd row 
Volatilitycolors = ['green' if dfpl.Open[i] < dfpl.Close[i] else 'red' for i in range(len(dfpl))]

fig.add_trace(go.Bar(x=dfpl.index, y=dfpl['Volatility'], marker_color=Volatilitycolors, showlegend=False), row=6, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['2'],
                         line=dict(color='red', width=1) ,showlegend=False
                        ), row=6, col=1)


fig.update_yaxes(title_text="Volatility", row=6, col=1)


# Plot xWAD trace on 6nd row 
fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl.xWAD,
                         line=dict(color='blue', width=1) ,showlegend=False
                        ), row=7, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['0'],
                         line=dict(color='red', width=1) ,showlegend=False
                        ), row=7, col=1)


fig.update_yaxes(title_text="xWAD", row=7, col=1)


# Plot MACD trace on 7rd row
MACDhcolors = ['green' if dfpl.MACDh_8_21_5[i] >= 0 else 'red' for i in range(len(dfpl))]

fig.add_trace(go.Bar(x=dfpl.index, 
                     y=dfpl.MACDh_8_21_5, 
                     marker_color= MACDhcolors, 
                     showlegend=False
                     ), row=8, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl.MACD_8_21_5,
                         line=dict(color='black', width=2),
                         showlegend=False
                        ), row=8, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl.MACDs_8_21_5,
                         line=dict(color='blue', width=1), 
                         showlegend=False
                        ), row=8, col=1)

fig.update_yaxes(title_text="MACD", showgrid=False, row=8, col=1)


# Plot TTMSqueeze trace on 8rd row
TTMhcolors = ['green' if dfpl.TTMSqueeze[i] >= 0 else 'red' for i in range(len(dfpl))]
fig.add_trace(go.Bar(x=dfpl.index, 
                     y=dfpl.TTMSqueeze, 
                     marker_color= TTMhcolors, 
                     showlegend=False
                     ), row=9, col=1)

fig.update_yaxes(title_text="TTMSqueeze", showgrid=False, row=9, col=1)


# Plot stochastics trace on 9th row
fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl.STOCHRSIk_21_5_13_8,
                         line=dict(color='black', width=2) ,showlegend=False
                        ), row=10, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl.STOCHRSId_21_5_13_8,
                         line=dict(color='blue', width=1) ,showlegend=False
                        ), row=10, col=1)

# Plot stochastics line levels trace on 9th row
fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['20'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=10, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['50'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=10, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['80'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=10, col=1)

fig.update_yaxes(title_text="STOCH RSI", row=10, col=1, range = [0, 100])

# Plot TSI trace on 10th row
fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl.TSI_30_8_13,
                         line=dict(color='black', width=2) ,showlegend=False
                        ), row=11, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['-20'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=11, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['20'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=11, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['-50'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=11, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['50'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=11, col=1)

fig.update_yaxes(title_text="TSI", row=11, col=1, range = [-70, 70])


# Plot RSI trace on 11th row
fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl.RSI,
                         line=dict(color='black', width=2) ,showlegend=False
                        ), row=12, col=1)


fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['20'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=12, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['40'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=12, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['60'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=12, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['80'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=12, col=1)


fig.update_yaxes(title_text=" RSI", row=12, col=1, range = [0, 100])

# Plot RVI trace on 12th row
fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl.RVI,
                         line=dict(color='black', width=2) ,showlegend=False
                        ), row=13, col=1)


fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['20'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=13, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['40'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=13, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['60'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=13, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['80'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=13, col=1)


fig.update_yaxes(title_text="RVI", row=13, col=1, range = [0, 100])

# Plot MFI trace on 13th row
fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.MFI, line=dict(color='black', width=2) ,showlegend=False), row=14, col=1)


fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['20'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=14, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['40'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=14, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['60'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=14, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['80'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=14, col=1)

fig.update_yaxes(title_text="MFI", row=14, col=1, range = [0, 100])

# Plot WaveTrend trace on 14th row
fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.wt1, line=dict(color='blue', width=2) ,showlegend=False), row=15, col=1)

fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.wt2, line=dict(color='red', width=2) ,showlegend=False), row=15, col=1)


fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['60'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=15, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['50'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=15, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['0'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=15, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['-50'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=15, col=1)

fig.add_trace(go.Scatter(x=dfpl.index,
                         y=dfpl['-60'],
                         line=dict(color='black', width=1) ,showlegend=False
                        ), row=15, col=1)


fig.update_yaxes(title_text="WaveTrend", row=15, col=1, range = [-90, 90])


# Plot WeisWaveVolume trace on 15rd row
WeisWaveVolumeColor = ['green' if dfpl.plotWWV[i] >= 0 else 'red' for i in range(len(dfpl))]
fig.add_trace(go.Bar(x=dfpl.index, 
                     y=dfpl.plotWWV, 
                     marker_color= WeisWaveVolumeColor, 
                     showlegend=False
                     ), row=16, col=1)


fig.update_yaxes(title_text="Weis Wave Volume", showgrid=False, row=16, col=1)


fig.update_layout(
    autosize=True,
    width=5000,
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
                 )

fig.show()

# %%
#df.to_excel("C:\\Users\\MC\\OneDrive\\CryptoPro\\src\\CodesForTest\\ETHUSDT4h.xlsx")

#df.to_csv("G:\\\My Drive\\\MyProjects\\\codes\\\ADAUSDT4h.csv")


