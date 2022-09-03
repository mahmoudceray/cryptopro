from binance import Client
import pandas as pd
import requests
import time
import websocket as ws
import warnings

api_key = 'yUyxMgVpkAcIzGYAKBAKanszbdSdEv9m3BuCZJCtPdlbBxyU2HEKur7CSQ8d5yUn'
api_secret = '0jJsHsSIsvIzASZ8VgnKUUBsC40ztLERXzAryKnzDzpTTxDcFlqzJIsYjUsFgU2P'
bot_key = '5746703295:AAHJBZYe7XCCyc6wFBgyp2jxRp8tAwrFwDM'
chat_id = '929825457'

clinet = Client(api_key, api_secret)


def send_update(mssg):
    url = "https://api.telegram.org/bot5746703295:AAHJBZYe7XCCyc6wFBgyp2jxRp8tAwrFwDM/sendMessage?chat_id=929825457&text={}".format(
        mssg)
    requests.get(url)


def getdata(symbol, interval, lookback):

    df = pd.DataFrame(clinet.get_historical_klines(symbol, interval, lookback))

    df.columns = ["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time", "Quote asset volume",
                  "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"]
    df = df.iloc[:, :8]
    df = df.set_index('Open Time')
    df.index = pd.to_datetime(df.index, unit='ms')
    df.index = df.index + pd.Timedelta(hours=3)
    df = df.astype(float)
    df.index

    return df


async def pingpong():
    pong_waiter = await ws.ping()
    return await pong_waiter


#intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1mo']

intervals = ['1m']
coins = ['ADAUSDT', 'ADXUSDT', 'AIONUSDT', 'ALGOUSDT', 'ALICEUSDT', 'ALPINEUSDT', 'ANKRUSDT', 'ANTUSDT', 'API3USDT', 'ARPAUSDT', 'ARUSDT', 'ASRUSDT', 'ATAUSDT', 'ATOMUSDT', 'AVAUSDT', 'AVAXUSDT', 'AXSUSDT',
         'BALUSDT', 'BANDUSDT', 'BATUSDT', 'BCHUSDT', 'BEAMUSDT', 'BLZUSDT', 'BSWUSDT', 'BTCUSDT', 'BTTCUSDT', 'CELOUSDT', 'CELRUSDT', 'CFXUSDT', 'CHRUSDT', 'CHZUSDT', 'CKBUSDT', 'COCOSUSDT', 'COSUSDT',
         'COTIUSDT', 'CTKUSDT', 'CTSIUSDT', 'CTXCUSDT', 'CVCUSDT', 'DASHUSDT', 'DATAUSDT', 'DCRUSDT', 'DEGOUSDT', 'DENTUSDT', 'DGBUSDT', 'DNTUSDT', 'DOCKUSDT', 'DOGEUSDT', 'DOTUSDT', 'DREPUSDT', 'DUSKUSDT',
         'EGLDUSDT', 'ELFUSDT', 'ENJUSDT', 'ENSUSDT', 'EOSUSDT', 'ETCUSDT', 'ETHUSDT', 'FETUSDT', 'FILUSDT', 'FIOUSDT', 'FIROUSDT', 'FLOWUSDT', 'FTMUSDT', 'FXSUSDT', 'GALAUSDT', 'GRTUSDT', 'GTCUSDT', 'GTOUSDT',
         'HBARUSDT', 'HIVEUSDT', 'HNTUSDT', 'HOTUSDT', 'ICPUSDT', 'ICXUSDT', 'IOSTUSDT', 'IOTAUSDT', 'IOTXUSDT', 'IRISUSDT', 'JASMYUSDT', 'KDAUSDT', 'KEYUSDT', 'KLAYUSDT', 'KMDUSDT', 'KSMUSDT', 'LINKUSDT',
         'LITUSDT', 'LSKUSDT', 'LTCUSDT', 'LTOUSDT', 'MANAUSDT', 'MASKUSDT', 'MATICUSDT', 'MBLUSDT', 'MCUSDT', 'MDTUSDT', 'MINAUSDT', 'MOBUSDT', 'MTLUSDT', 'MULTIUSDT', 'NEARUSDT', 'NKNUSDT', 'NULSUSDT',
         'OCEANUSDT', 'OGNUSDT', 'OMGUSDT', 'ONEUSDT', 'ONGUSDT', 'ONGUSDT', 'OPUSDT', 'ORNUSDT', 'OXTUSDT', 'PAXGUSDT', 'PEOPLEUSDT', 'PERLUSDT', 'PHAUSDT', 'PNTUSDT', 'PONDUSDT', 'POWRUSDT', 'PUNDIXUSDT',
         'QNTUSDT', 'QTUMUSDT', 'RADUSDT', 'REQUSDT', 'RIFUSDT', 'ROSEUSDT', 'RSRUSDT', 'RVNUSDT', 'SANDUSDT', 'SCRTUSDT', 'SCUSDT', 'SFPUSDT', 'SKLUSDT', 'SOLUSDT', 'STMXUSDT', 'STORJUSDT', 'STRAXUSDT',
         'STXUSDT', 'SXPUSDT', 'SYSUSDT', 'TFUELUSDT', 'THETAUSDT', 'TOMOUSDT', 'TORNUSDT', 'TRBUSDT', 'TRXUSDT', 'TVKUSDT', 'TWTUSDT', 'UTKUSDT', 'VETUSDT', 'VGXUSDT', 'VIDTUSDT', 'VTHOUSDT', 'WAVESUSDT',
         'WAXPUSDT', 'WTCUSDT', 'XECUSDT', 'XEMUSDT', 'XLMUSDT', 'XMRUSDT', 'XNOUSDT', 'XRPUSDT', 'XTZUSDT', 'ZECUSDT', 'ZENUSDT', 'ZILUSDT']

print("RUN")

while True:

    coindata = pd.DataFrame()

    for coin in coins:
        for interval in intervals:
            coindata = getdata(coin, interval, "1 day ago UTC")
            coindata = coindata.iloc[-3:].replace(0, 1)

            VolumeDiff = (coindata['Volume'].iloc[1:].reset_index(
                drop=True) / coindata['Volume'].iloc[0:].reset_index(drop=True)) >= 2.0

            VolumeDiff1 = (coindata['Volume'].iloc[1:].reset_index(
                drop=True) / coindata['Volume'].iloc[0:].reset_index(drop=True))

            PriceDiff = coindata['Close'].iloc[1:].reset_index(
                drop=True) > coindata['Open'].iloc[1:].reset_index(drop=True)

            QuoteAssetVolume = coindata['Quote asset volume'].iloc[:]

            if VolumeDiff.loc[1] and PriceDiff.loc[1] and (QuoteAssetVolume[2] >= 40000.0):

                msg = '''{}
                
{},  {}

{}

VolumeDiff = {}
PriceDiff = {}
Asset Volume = {}


'''.format("Pump Signal", coin, interval, coindata.index[2], str("{:.2f}".format(VolumeDiff1[1])), PriceDiff[1], str("{:.2f}".format(QuoteAssetVolume[2])))

                print(msg)
                send_update(msg)

    try:
        pingpong()
    except:
        warnings.filterwarnings("ignore")
        continue

    time.sleep(0.1)
