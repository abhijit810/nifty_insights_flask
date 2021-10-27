import datetime

from flask import Flask, render_template
import pandas as pd
import gcsfs

pd.options.display.float_format = '${:,.2f}'.format
nifty = pd.read_csv("data.csv", index_col="Date")

fs = gcsfs.GCSFileSystem(project='data-science-gcp-324204')
with fs.open('nifty-data-bucket/data.csv') as f:
    nifty = pd.read_csv(f)
nifty[nifty['High'] > (nifty['Low'] * 1.03 )]
column_names = tuple(nifty.columns)
nifty_list = [[i for i in x if pd.notnull(i)] for x in nifty.tail().values.tolist()]

nifty.index = pd.to_datetime(nifty["Date"])
volatile_df = nifty[nifty['High'] >= (nifty['Low'] * 1.04 )]
volatile_list = [[i for i in x if pd.notnull(i)] for x in volatile_df.values.tolist()]
insights = nifty[nifty.index.weekday.isin([0,1,2,3,4])]['Close'].describe()
insights_index = insights.index.tolist()

make_float = lambda x: "{:,.2f}".format(x)
# insights_values = insights.values.tolist()
insights_values = [str(a) for a in insights.apply(make_float)]
#graph_index = nifty.index.tolist()
#graph_data = nifty["High"].values.tolist()
open = nifty["Open"]
monthly_rolling = nifty['Close'].rolling('30d').mean().values.tolist()
indexes = [date_obj.strftime("%d-%m-%Y") for date_obj in open.index.tolist()]
print(nifty)