from binance import Client
import pandas as pd
import requests
import time
import websocket as ws
import warnings

api_key = 'M6itnCp9Nuno8t3oMkNbeiDsi2KAqZanFs7TwwSMyRhae6ZiW148aveGY9YSIN6i'
api_secret = 'KPKJLV3keJhofpM4k4DgOChvMZBhUUa66il2pIc0iVNlMkG4UhuDg5lNmTrqlkjU'
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
coins = ['ADABTC', 'ADXBTC', 'AERGOBTC', 'AIONBTC', 'ALGOBTC', 'ALICEBTC', 'ALPINEBTC', 'AMPBTC', 'ANKRBTC', 'ANTBTC', 'API3BTC', 'ARBTC', 'ARPABTC', 'ASRBTC', 'ATABTC', 'ATOMBTC', 'AVABTC', 'AVAXBTC',
         'AXSBTC', 'BALBTC', 'BANDBTC', 'BATBTC', 'BCHBTC', 'BEAMBTC', 'BLZBTC', 'CELOBTC', 'CELRBTC', 'CFXBTC', 'CHRBTC', 'CHZBTC', 'COSBTC', 'COTIBTC', 'CTKBTC', 'CTSIBTC', 'CTXCBTC', 'CVCBTC', 'DASHBTC',
         'DATABTC', 'DCRBTC', 'DEGOBTC', 'DGBBTC', 'DNTBTC', 'DOCKBTC', 'DOGEBTC', 'DOTBTC', 'DREPBTC', 'DUSKBTC', 'EGLDBTC', 'ELFBTC', 'ENJBTC', 'ENSBTC', 'EOSBTC', 'ETCBTC', 'ETHBTC', 'FETBTC', 'FILBTC',
         'FIOBTC', 'FIROBTC', 'FLOWBTC', 'FLUXBTC', 'FTMBTC', 'FXSBTC', 'GALABTC', 'GMTBTC', 'GRTBTC', 'GTCBTC', 'GTOBTC', 'HBARBTC', 'HIVEBTC', 'HNTBTC', 'ICPBTC', 'ICXBTC', 'IOSTBTC', 'IOTABTC', 'IOTXBTC',
         'IRISBTC', 'JASMYBTC', 'KDABTC', 'KLAYBTC', 'KMDBTC', 'KSMBTC', 'LINKBTC', 'LITBTC', 'LOOMBTC', 'LRCBTC', 'LSKBTC', 'LTCBTC', 'LTOBTC', 'MANABTC', 'MATICBTC', 'MCBTC', 'MDTBTC', 'MINABTC', 'MOBBTC',
         'MTLBTC', 'MULTIBTC', 'NEARBTC', 'NEBLBTC', 'NKNBTC', 'NULSBTC', 'OCEANBTC', 'OGNBTC', 'OMGBTC', 'ONEBTC', 'ONGBTC', 'ONGBTC', 'OPBTC', 'ORNBTC', 'OXTBTC', 'PAXGBTC', 'PEOPLEBTC', 'PERLBTC', 'PHABTC',
         'PHBBTC', 'PIVXBTC', 'PNTBTC', 'PONDBTC', 'POWRBTC', 'PROMBTC', 'QLCBTC', 'QNTBTC', 'QTUMBTC', 'RADBTC', 'REQBTC', 'RIFBTC', 'RLCBTC', 'ROSEBTC', 'RVNBTC', 'SANDBTC', 'SCRTBTC', 'SFPBTC', 'SKLBTC',
         'SOLBTC', 'STMXBTC', 'STORJBTC', 'STRAXBTC', 'STXBTC', 'SXPBTC', 'SYSBTC', 'TFUELBTC', 'THETABTC', 'TOMOBTC', 'TORNBTC', 'TRBBTC', 'TRXBTC', 'TVKBTC', 'TWTBTC', 'UTKBTC', 'VETBTC', 'VGXBTC', 'VIDTBTC',
         'WABIBTC', 'WAVESBTC', 'WAXPBTC', 'WTCBTC', 'XEMBTC', 'XLMBTC', 'XMRBTC', 'XNOBTC', 'XRPBTC', 'XTZBTC', 'ZECBTC', 'ZENBTC', 'ZILBTC']

print("RUN")

while True:

    coindata = pd.DataFrame()

    for coin in coins:
        for interval in intervals:
            coindata = getdata(coin, interval, "1 day ago UTC")
            coindata = coindata.iloc[-3:].replace(0, 1)

            VolumeDiff = (coindata['Volume'].iloc[1:].reset_index(
                drop=True) / coindata['Volume'].iloc[0:].reset_index(drop=True)) >= 1.0

            VolumeDiff1 = (coindata['Volume'].iloc[1:].reset_index(
                drop=True) / coindata['Volume'].iloc[0:].reset_index(drop=True))

            PriceDiff = coindata['Close'].iloc[1:].reset_index(
                drop=True) > coindata['Open'].iloc[1:].reset_index(drop=True)

            QuoteAssetVolume = coindata['Quote asset volume'].iloc[:]

            if VolumeDiff.loc[1] and PriceDiff.loc[1] and (QuoteAssetVolume[2] >= 2.0):

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
