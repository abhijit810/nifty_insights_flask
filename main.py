import datetime

from flask import Flask, render_template
import pandas as pd
app = Flask(__name__)


@app.route('/')
def root():
    pd.options.display.float_format = '${:,.2f}'.format
    nifty = pd.read_csv("data.csv", index_col =0)
    nifty[nifty['High'] > (nifty['Low'] * 1.03 )]

    column_names = tuple(nifty.columns)
    nifty_list = [[i for i in x if pd.notnull(i)] for x in nifty.tail().values.tolist()]
    
    nifty.index = pd.to_datetime(nifty.index)
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

    return render_template('index.html', data=nifty_list, 
                                         headers=column_names, 
                                         volatile=volatile_list, 
                                         insights=[insights_index] + [insights_values],
                                         labels = indexes,
                                         values = open.values.tolist(),
                                         rolling = monthly_rolling
                                        )


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)