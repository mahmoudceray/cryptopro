import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plotchart(df, FirstCandle, LastCandle, coin, time, colums=1, c=1, heights1=9, heights2=3):

    dfpl = df[FirstCandle: LastCandle]

    # first declare an empty figure
    fig = go.Figure()
    # Plot OHLC on 1st subplot (using the codes from before)

    fig = make_subplots(rows=16, cols=colums, shared_xaxes=False,
                        vertical_spacing=0.01,
                        row_heights=[heights1, heights1, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2])

    # add OHLC trace1 من حط لوب حتى نطالع شارتين تحت بعض
    fig.add_trace(go.Candlestick(x=dfpl.index,
                                 open=dfpl['Open'],
                                 high=dfpl['High'],
                                 low=dfpl['Low'],
                                 close=dfpl['Close'],
                                 showlegend=True,
                                 name="{} {}".format(coin, time)), row=1, col=c)

    # add ATR SUPERTREND trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['SUPERT_8_2.618'], line=dict(
        color='orange', width=1), name="ATR"), row=1, col=c)

    # add LINEAR REGRESSION  Long Trend trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.lts, line=dict(
        color='black', width=1), name="Long Trend"), row=1, col=c)

    # add LINEAR REGRESSION  Long Trend trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.Highlts, line=dict(
        color='red', width=2), name="High Long Trend"), row=1, col=c)

    # add LINEAR REGRESSION  Long Trend trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.Lowlts, line=dict(
        color='green', width=2), name="Low Long Trend"), row=1, col=c)

    # add Linear Regression Channel trace
    #line=dict(color='purple', width=1)

    fig.add_trace(go.Scatter(x=[dfpl.index[-150], dfpl.index[-1]], y=[
                  dfpl.y1RegCh2[-1], dfpl.y2RegCh2[-1]], mode="lines", name="RegChUp"), row=1, col=c)

    fig.add_trace(go.Scatter(x=[dfpl.index[-150], dfpl.index[-1]], y=[
                  dfpl.y1RegCh1[-1], dfpl.y2RegCh1[-1]], mode="lines", name="RegChMid"), row=1, col=c)

    fig.add_trace(go.Scatter(x=[dfpl.index[-150], dfpl.index[-1]], y=[
                  dfpl.y1RegCh0[-1], dfpl.y2RegCh0[-1]], mode="lines", name="RegChDown"), row=1, col=c)

    # add Support & Resistance Lines trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.ph1, line=dict(
        color='red', width=2), name="Support Line"), row=1, col=c)
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.pll, line=dict(
        color='blue', width=2), name="Resistance Line"), row=1, col=c)

    # end of OHLC trace1 ========================================================================================

    # add OHLC trace1 من حط لوب حتى نطالع شارتين تحت بعض
    fig.add_trace(go.Candlestick(x=dfpl.index,
                                 open=dfpl['Open'],
                                 high=dfpl['High'],
                                 low=dfpl['Low'],
                                 close=dfpl['Close'],
                                 showlegend=True,
                                 name="{} {}".format(coin, time)), row=2, col=c)

    fig.update_yaxes(title_text=f"{coin} {time}", row=2, col=c)

    # Plot Quote asset volume trace on 2th row
    #"cumsum net asset volume"
    #"net asset volume"
    netvolumecolors = ['green' if dfpl["net asset volume"]
                       [i] > 0 else 'red' for i in range(len(dfpl))]
    fig.add_trace(go.Bar(x=dfpl.index, y=dfpl["net asset volume"],
                  marker_color=netvolumecolors, showlegend=False), row=3, col=c)

    fig.update_yaxes(title_text="net asset volume", row=3, col=c)

    # Plot volume trace on 3nd row
    Volumecolors = ['green' if dfpl.Open[i] <
                    dfpl.Close[i] else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(
        x=dfpl.index, y=dfpl["Volume"], marker_color=Volumecolors, showlegend=False), row=4, col=c)

    fig.update_yaxes(title_text="Volume", row=4, col=c)

    # Plot Buy VOLUME trace on 4nd row
    fig.add_trace(go.Bar(
        x=dfpl.index, y=dfpl['BVOLUME'], marker_color='green', showlegend=False), row=5, col=c)
    fig.update_yaxes(title_text="B/S Volume", row=5, col=c)

    # Plot Sell volume trace on 4nd row
    fig.add_trace(go.Bar(
        x=dfpl.index, y=dfpl['SVOLUME'], marker_color='red', showlegend=False), row=5, col=c)
    fig.update_yaxes(title_text="B/S Volume", row=5, col=c)

    # Plot Volatility trace on 5nd row
    Volatilitycolors = ['green' if dfpl.Open[i] <
                        dfpl.Close[i] else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(x=dfpl.index, y=dfpl['Volatility'],
                  marker_color=Volatilitycolors, showlegend=False), row=6, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['2'],
                             line=dict(color='red', width=1), showlegend=False
                             ), row=6, col=c)

    fig.update_yaxes(title_text="Volatility", row=6, col=c)

    # Plot xWAD trace on 6nd row
    xWADcolors = ['green' if dfpl.xWAD[i] >=
                  0 else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl.xWAD,
                         marker_color=xWADcolors, showlegend=False
                         ), row=7, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['0'],
                             line=dict(color='red', width=1), showlegend=False
                             ), row=7, col=c)

    fig.update_yaxes(title_text="xWAD", row=7, col=c)

    # Plot MACD trace on 7rd row
    MACDhcolors = ['green' if dfpl.MACDh_8_21_5[i]
                   >= 0 else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl.MACDh_8_21_5,
                         marker_color=MACDhcolors,
                         showlegend=False
                         ), row=8, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.MACD_8_21_5,
                             line=dict(color='black', width=2),
                             showlegend=False
                             ), row=8, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.MACDs_8_21_5,
                             line=dict(color='blue', width=1),
                             showlegend=False
                             ), row=8, col=c)

    fig.update_yaxes(title_text="MACD", showgrid=False, row=8, col=c)

    # Plot TTMSqueeze trace on 8rd row
    TTMhcolors = ['green' if dfpl["SQZPRO_13_2.0_13_2_1.5_1"]
                  [i] >= 0 else 'red' for i in range(len(dfpl))]
    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl["SQZPRO_13_2.0_13_2_1.5_1"],
                         marker_color=TTMhcolors,
                         showlegend=False
                         ), row=9, col=c)

    fig.update_yaxes(title_text="TTMSqueeze", showgrid=False, row=9, col=c)

    # Plot stochastics trace on 9th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.STOCHRSIk_21_5_13_8,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=10, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.STOCHRSId_21_5_13_8,
                             line=dict(color='blue', width=1), showlegend=False
                             ), row=10, col=c)

    # Plot stochastics line levels trace on 9th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=10, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=10, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=10, col=c)

    fig.update_yaxes(title_text="STOCH RSI", row=10, col=c, range=[0, 100])

    # Plot TSI trace on 10th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.TSI_30_8_13,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.update_yaxes(title_text="TSI", row=11, col=c, range=[-70, 70])

    # Plot RSI trace on 11th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.RSI,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['40'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.update_yaxes(title_text=" RSI", row=12, col=c, range=[0, 100])

    # Plot RVI trace on 12th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.RVI,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['40'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.update_yaxes(title_text="RVI", row=13, col=c, range=[0, 100])

    # Plot MFI trace on 13th row
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.MFI, line=dict(
        color='black', width=2), showlegend=False), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['40'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.update_yaxes(title_text="MFI", row=14, col=c, range=[0, 100])

    # Plot WaveTrend trace on 14th row
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.wt1, line=dict(
        color='blue', width=2), showlegend=False), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.wt2, line=dict(
        color='red', width=2), showlegend=False), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['0'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.update_yaxes(title_text="WaveTrend", row=15, col=c, range=[-90, 90])

    # Plot WeisWaveVolume trace on 15rd row
    WeisWaveVolumeColor = ['green' if dfpl.plotWWV[i]
                           >= 0 else 'red' for i in range(len(dfpl))]
    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl.plotWWV,
                         marker_color=WeisWaveVolumeColor,
                         showlegend=False
                         ), row=16, col=c)

    fig.update_yaxes(title_text="Weis Wave Volume",
                     showgrid=False, row=16, col=c)

    fig.update_layout(
        autosize=True,
        width=7000,
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
                      yaxis1={'side': 'right'},
                      yaxis2={'side': 'right'},
                      yaxis3={'side': 'right'},
                      yaxis4={'side': 'right'},
                      yaxis5={'side': 'right'},
                      yaxis6={'side': 'right'},
                      yaxis7={'side': 'right'},
                      yaxis8={'side': 'right'},
                      yaxis9={'side': 'right'},
                      yaxis10={'side': 'right'},
                      yaxis11={'side': 'right'},
                      yaxis12={'side': 'right'},
                      yaxis13={'side': 'right'},
                      yaxis14={'side': 'right'},
                      yaxis15={'side': 'right'},
                      yaxis16={'side': 'right'},
                      )

    fig.show()


def PlotCharts(df, FirstCandle, LastCandle, coin, time, colums=1, c=1, heights1=9, heights2=3):

    dfpl = df[FirstCandle: LastCandle]

    # first declare an empty figure
    # Plot OHLC on 1st subplot (using the codes from before)

    fig = make_subplots(rows=16, cols=colums, shared_xaxes=False,
                        vertical_spacing=0.01,
                        row_heights=[heights1, heights1, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2, heights2])

    # add OHLC trace1 من حط لوب حتى نطالع شارتين تحت بعض
    fig.add_trace(go.Candlestick(x=dfpl.index,
                                 open=dfpl['Open'],
                                 high=dfpl['High'],
                                 low=dfpl['Low'],
                                 close=dfpl['Close'],
                                 showlegend=True,
                                 name="{} {}".format(coin, time)), row=1, col=c)

    # add ATR SUPERTREND trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['SUPERT_8_2.618'], line=dict(
        color='orange', width=1), name="ATR"), row=1, col=c)

    # add LINEAR REGRESSION  Long Trend trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.lts, line=dict(
        color='black', width=1), name="Long Trend"), row=1, col=c)

    # add LINEAR REGRESSION  Long Trend trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.Highlts, line=dict(
        color='red', width=2), name="High Long Trend"), row=1, col=c)

    # add LINEAR REGRESSION  Long Trend trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.Lowlts, line=dict(
        color='green', width=2), name="Low Long Trend"), row=1, col=c)

    # add Linear Regression Channel trace
    #line=dict(color='purple', width=1)

    fig.add_trace(go.Scatter(x=[dfpl.index[-150], dfpl.index[-1]], y=[
                  dfpl.y1RegCh2[-1], dfpl.y2RegCh2[-1]], mode="lines", name="RegChUp"), row=1, col=c)

    fig.add_trace(go.Scatter(x=[dfpl.index[-150], dfpl.index[-1]], y=[
                  dfpl.y1RegCh1[-1], dfpl.y2RegCh1[-1]], mode="lines", name="RegChMid"), row=1, col=c)

    fig.add_trace(go.Scatter(x=[dfpl.index[-150], dfpl.index[-1]], y=[
                  dfpl.y1RegCh0[-1], dfpl.y2RegCh0[-1]], mode="lines", name="RegChDown"), row=1, col=c)

    # add Support & Resistance Lines trace
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.ph1, line=dict(
        color='red', width=2), name="Support Line"), row=1, col=c)
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.pll, line=dict(
        color='blue', width=2), name="Resistance Line"), row=1, col=c)

    # end of OHLC trace1 ========================================================================================

    # add OHLC trace1 من حط لوب حتى نطالع شارتين تحت بعض
    fig.add_trace(go.Candlestick(x=dfpl.index,
                                 open=dfpl['Open'],
                                 high=dfpl['High'],
                                 low=dfpl['Low'],
                                 close=dfpl['Close'],
                                 showlegend=True,
                                 name="{} {}".format(coin, time)), row=2, col=c)

    fig.update_yaxes(title_text=f"{coin} {time}", row=2, col=c)

    # Plot Quote asset volume trace on 2th row
    #"cumsum net asset volume"
    #"net asset volume"
    netvolumecolors = ['green' if dfpl["net asset volume"]
                       [i] > 0 else 'red' for i in range(len(dfpl))]
    fig.add_trace(go.Bar(x=dfpl.index, y=dfpl["net asset volume"],
                  marker_color=netvolumecolors, showlegend=False), row=3, col=c)

    fig.update_yaxes(title_text="net asset volume", row=3, col=c)

    # Plot volume trace on 3nd row
    Volumecolors = ['green' if dfpl.Open[i] <
                    dfpl.Close[i] else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(
        x=dfpl.index, y=dfpl["Volume"], marker_color=Volumecolors, showlegend=False), row=4, col=c)

    fig.update_yaxes(title_text="Volume", row=4, col=c)

    # Plot Buy VOLUME trace on 4nd row
    fig.add_trace(go.Bar(
        x=dfpl.index, y=dfpl['BVOLUME'], marker_color='green', showlegend=False), row=5, col=c)
    fig.update_yaxes(title_text="B/S Volume", row=5, col=c)

    # Plot Sell volume trace on 4nd row
    fig.add_trace(go.Bar(
        x=dfpl.index, y=dfpl['SVOLUME'], marker_color='red', showlegend=False), row=5, col=c)
    fig.update_yaxes(title_text="B/S Volume", row=5, col=c)

    # Plot Volatility trace on 5nd row
    Volatilitycolors = ['green' if dfpl.Open[i] <
                        dfpl.Close[i] else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(x=dfpl.index, y=dfpl['Volatility'],
                  marker_color=Volatilitycolors, showlegend=False), row=6, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['2'],
                             line=dict(color='red', width=1), showlegend=False
                             ), row=6, col=c)

    fig.update_yaxes(title_text="Volatility", row=6, col=c)

    # Plot xWAD trace on 6nd row
    xWADcolors = ['green' if dfpl.xWAD[i] >=
                  0 else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl.xWAD,
                         marker_color=xWADcolors, showlegend=False
                         ), row=7, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['0'],
                             line=dict(color='red', width=1), showlegend=False
                             ), row=7, col=c)

    fig.update_yaxes(title_text="xWAD", row=7, col=c)

    # Plot MACD trace on 7rd row
    MACDhcolors = ['green' if dfpl.MACDh_8_21_5[i]
                   >= 0 else 'red' for i in range(len(dfpl))]

    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl.MACDh_8_21_5,
                         marker_color=MACDhcolors,
                         showlegend=False
                         ), row=8, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.MACD_8_21_5,
                             line=dict(color='black', width=2),
                             showlegend=False
                             ), row=8, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.MACDs_8_21_5,
                             line=dict(color='blue', width=1),
                             showlegend=False
                             ), row=8, col=c)

    fig.update_yaxes(title_text="MACD", showgrid=False, row=8, col=c)

    # Plot TTMSqueeze trace on 8rd row
    TTMhcolors = ['green' if dfpl["SQZPRO_13_2.0_13_2_1.5_1"]
                  [i] >= 0 else 'red' for i in range(len(dfpl))]
    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl["SQZPRO_13_2.0_13_2_1.5_1"],
                         marker_color=TTMhcolors,
                         showlegend=False
                         ), row=9, col=c)

    fig.update_yaxes(title_text="TTMSqueeze", showgrid=False, row=9, col=c)

    # Plot stochastics trace on 9th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.STOCHRSIk_21_5_13_8,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=10, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.STOCHRSId_21_5_13_8,
                             line=dict(color='blue', width=1), showlegend=False
                             ), row=10, col=c)

    # Plot stochastics line levels trace on 9th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=10, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=10, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=10, col=c)

    fig.update_yaxes(title_text="STOCH RSI", row=10, col=c, range=[0, 100])

    # Plot TSI trace on 10th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.TSI_30_8_13,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=11, col=c)

    fig.update_yaxes(title_text="TSI", row=11, col=c, range=[-70, 70])

    # Plot RSI trace on 11th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.RSI,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['40'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=12, col=c)

    fig.update_yaxes(title_text=" RSI", row=12, col=c, range=[0, 100])

    # Plot RVI trace on 12th row
    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl.RVI,
                             line=dict(color='black', width=2), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['40'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=13, col=c)

    fig.update_yaxes(title_text="RVI", row=13, col=c, range=[0, 100])

    # Plot MFI trace on 13th row
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.MFI, line=dict(
        color='black', width=2), showlegend=False), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['20'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['40'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['80'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=14, col=c)

    fig.update_yaxes(title_text="MFI", row=14, col=c, range=[0, 100])

    # Plot WaveTrend trace on 14th row
    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.wt1, line=dict(
        color='blue', width=2), showlegend=False), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl.wt2, line=dict(
        color='red', width=2), showlegend=False), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['0'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-50'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.add_trace(go.Scatter(x=dfpl.index,
                             y=dfpl['-60'],
                             line=dict(color='black', width=1), showlegend=False
                             ), row=15, col=c)

    fig.update_yaxes(title_text="WaveTrend", row=15, col=c, range=[-90, 90])

    # Plot WeisWaveVolume trace on 15rd row
    WeisWaveVolumeColor = ['green' if dfpl.plotWWV[i]
                           >= 0 else 'red' for i in range(len(dfpl))]
    fig.add_trace(go.Bar(x=dfpl.index,
                         y=dfpl.plotWWV,
                         marker_color=WeisWaveVolumeColor,
                         showlegend=False
                         ), row=16, col=c)

    fig.update_yaxes(title_text="Weis Wave Volume",
                     showgrid=False, row=16, col=c)

    fig.update_layout(
        autosize=True,
        width=7000,
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
                      yaxis1={'side': 'right'},
                      yaxis2={'side': 'right'},
                      yaxis3={'side': 'right'},
                      yaxis4={'side': 'right'},
                      yaxis5={'side': 'right'},
                      yaxis6={'side': 'right'},
                      yaxis7={'side': 'right'},
                      yaxis8={'side': 'right'},
                      yaxis9={'side': 'right'},
                      yaxis10={'side': 'right'},
                      yaxis11={'side': 'right'},
                      yaxis12={'side': 'right'},
                      yaxis13={'side': 'right'},
                      yaxis14={'side': 'right'},
                      yaxis15={'side': 'right'},
                      yaxis16={'side': 'right'},
                      )
