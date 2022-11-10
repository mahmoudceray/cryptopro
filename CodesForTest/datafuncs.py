import pandas as pd
import datetime
from binance import Client


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
