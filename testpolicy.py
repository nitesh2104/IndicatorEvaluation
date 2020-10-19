import datetime as dt

import TheoreticallyOptimalStrategy as tos

df_trades = tos.testPolicy(symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)
