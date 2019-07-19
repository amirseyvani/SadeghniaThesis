from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime

def dash_date(da):
    y = da[0:4]
    m = da[4:6]
    d = da[6:8]
    return str(y)+'-'+str(m)+'-'+str(d)


def  edit_date(df):
    df['Date'][:] = [dash_date(str(da)) for da in df['Date']]
    return df

df = edit_date(pd.read_csv('Data/sfars.csv'))

trace = go.Candlestick(
    x=df['Date'],
    open=df['<OPEN>'],
    high=df['<HIGH>'],
    low=df['<LOW>'],
    close=df['<CLOSE>'],
    increasing=dict(line=dict(color= '#17BECF')),
    decreasing=dict(line=dict(color= '#7F7F7F'))
)

data = [trace]
plot(data, filename='styled_candlestick')