import talib

# حساب خط الدعم والمقاومة و اضافتها الى ملف موجود


def SupportResistance(df, senPP):

    ph1 = talib.MAX(df.High, senPP)
    pll = talib.MIN(df.Low, senPP)

    df['ph1'] = [ph1[i] if ph1[i] != 0 else ph1[i-1] for i in range(len(df))]
    df['pll'] = [pll[i] if pll[i] != 0 else pll[i-1] for i in range(len(df))]

    return df


def support(df1, l, n1, n2): #n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if(df1.low[i]>df1.low[i-1]):
            return 0
    for i in range(l+1,l+n2+1):
        if(df1.low[i]<df1.low[i-1]):
            return 0
    return 1

#support(df,46,3,2)

def resistance(df1, l, n1, n2): #n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if(df1.high[i]<df1.high[i-1]):
            return 0
    for i in range(l+1,l+n2+1):
        if(df1.high[i]>df1.high[i-1]):
            return 0
    return 1
#resistance(df, 30, 3, 5)


ss = []
rr = []
n1=2
n2=2
for row in range(3, 205): #len(df)-n2
    if support(df, row, n1, n2):
        ss.append((row,df.low[row]))
    if resistance(df, row, n1, n2):
        rr.append((row,df.high[row]))
        
plotlist1 = [x[1] for x in sr if x[2]==1]
plotlist2 = [x[1] for x in sr if x[2]==2]
plotlist1.sort()
plotlist2.sort()

for i in range(1,len(plotlist1)):
    if(i>=len(plotlist1)):
        break
    if abs(plotlist1[i]-plotlist1[i-1])<=0.005:
        plotlist1.pop(i)

for i in range(1,len(plotlist2)):
    if(i>=len(plotlist2)):
        break
    if abs(plotlist2[i]-plotlist2[i-1])<=0.005:
        plotlist2.pop(i)
plotlist2
#plt.hist(plotlist, bins=10, alpha=0.5)



s = 0
e = 200
dfpl = df[s:e]
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt

fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['open'],
                high=dfpl['high'],
                low=dfpl['low'],
                close=dfpl['close'])])

c=0
while (1):
    if(c>len(ss)-1 ):
        break
    fig.add_shape(type='line', x0=ss[c][0], y0=ss[c][1],
                  x1=e,
                  y1=ss[c][1],
                  line=dict(color="MediumPurple",width=3)
                  )
    c+=1

c=0
while (1):
    if(c>len(rr)-1 ):
        break
    fig.add_shape(type='line', x0=rr[c][0], y0=rr[c][1],
                  x1=e,
                  y1=rr[c][1],
                  line=dict(color="RoyalBlue",width=1)
                  )
    c+=1    

fig.show()