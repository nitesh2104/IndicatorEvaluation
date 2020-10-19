import matplotlib.pyplot as plt
import yfinance as yf

from util import get_data
import pandas as pd

"""
indicators.py Your code that implements your indicators as functions that operate on DataFrames.
The “main” code in indicators.py should generate the charts that illustrate your indicators in the report.

Use only the data provided for this course. You are not allowed to import external data.
- Please add in an author function to each file.
- For your report, use only the symbol JPM. This will enable us to more easily compare results.
- Use the time period January 1, 2008 to December 31 2009.
- Starting cash is $100,000.
- Allowable positions are: 1000 shares long, 1000 shares short, 0 shares.
- Benchmark: The performance of a portfolio starting with $100,000 cash, investing in 1000 shares of JPM and holding that position.
- There is no limit on leverage.
- Transaction costs for TheoreticallyOptimalStrategy: Commission: $0.00, Impact: 0.00.
- Correct trades df format used.

"""


def author():
    return "nitarora"


def calculate_SMA(port_val, window, plot=False):
    port_val = port_val/port_val.iloc[0]
    port_val["JPM_SMA"] = port_val['JPM'].rolling(window=window).mean()
    port_val['JPM_Price/SMA'] = port_val['JPM']/port_val['JPM_SMA']
    if plot:
        ax = port_val.plot(title='SMA (Simple Moving Average, Window=20 days)', fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Normalized Price")
        plt.grid(True, 'both')

        # plt.show()
        plt.savefig("SMA.jpg", dpi=500)


def calculate_BB(port_val, window, plot=False):
    port_val["JPM_SMA"] = port_val['JPM'].rolling(window=window).mean()
    std = port_val['JPM'].rolling(window=window).std()
    port_val["JPM_BB_U"] = port_val['JPM_SMA'] + 2 * std
    port_val["JPM_BB_L"] = port_val['JPM_SMA'] - 2 * std
    if plot:
        ax = port_val.plot(title='BB', fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        plt.show()


def calculate_momentum(port_val, window, plot=False):
    port_val = port_val/port_val.iloc[0]
    port_val['momentum'] = (port_val / port_val.shift(window)) - 1
    if plot:
        plt.rcParams['axes.grid'] = True
        plt.subplot(2, 1, 1)
        ax = port_val['JPM'].plot(title='Stock Price (JPM)', fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Normalized Price")

        plt.subplot(2, 1, 2)
        ax = port_val['momentum'].plot(title='Momentum, Window=20 days', fontsize=8, color='green')
        ax.set_xlabel("Date")
        # plt.show()
        plt.subplots_adjust(hspace=0.9)
        plt.savefig('momemtum.jpg', dpi=500)


def calculate_RSI_EMV(port_val, window, plot=False):
    diff = port_val.dropna().diff()
    diff = diff[1:]

    up_diff, down_diff = diff.copy(), diff.copy()

    up_diff[up_diff < 0] = 0
    down_diff[down_diff > 0] = 0

    total_average_gain = up_diff.ewm(span=window).mean()
    total_average_loss = down_diff.abs().ewm(span=window).mean()

    rs_emv = abs(total_average_gain / total_average_loss)

    port_val['RSI_EMV'] = 100.0 - 100.0 / (1.0 + rs_emv)

    if plot:
        plt.rcParams['axes.grid'] = True
        plt.subplot(2, 1, 1)
        ax = port_val['JPM'].plot(title='Stock Price (JPM)', fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")

        plt.subplot(2, 1, 2)
        ax = port_val['RSI_EMV'].plot(title='RSI (Relative Strength Index), Window: 14', fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")


        ax.axhline(70, color='green', lw=1)
        ax.axhline(30, color='red', lw=1)
        ax.fill_between(port_val.index, 0, 0, where=port_val['RSI_EMV'] < 70, facecolor='green')
        ax.fill_between(port_val.index, 0, 0, where=port_val['RSI_EMV'] > 30, facecolor='red')
        # plt.show()
        plt.subplots_adjust(hspace=0.9)
        plt.savefig("RSI.jpg", dpi=500)

def calculate_RSI_SMA(port_val, window, plot=False):
    diff = port_val.dropna().diff()
    diff = diff[1:]

    up_diff, down_diff = diff.copy(), diff.copy()

    up_diff[up_diff < 0] = 0
    down_diff[down_diff > 0] = 0

    total_average_gain = up_diff.rolling(window=window).mean()
    total_average_loss = down_diff.abs().rolling(window=window).mean()

    rs_sma = abs(total_average_gain / total_average_loss)

    port_val['RSI_SMA'] = 100.0 - 100.0 / (1.0 + rs_sma)

    if plot:
        plt.subplot(2, 1, 1)
        ax = port_val['JPM'].plot(title='BB', fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")

        plt.subplot(2, 1, 2)
        ax = port_val['RSI_SMA'].plot(title='BB', fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        plt.figure(dpi=1200)
        plt.show()


def calculate_zscore(port_val, window, plot=False):
    port_val['zscore'] = (port_val - port_val.rolling(window=window).mean()) / port_val.rolling(window=window).std()
    if plot:
        plt.subplot(2, 1, 1)
        ax = port_val['JPM'].plot(title='BB', fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")

        plt.subplot(2, 1, 2)
        ax = port_val['zscore'].plot(title='BB', fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        plt.figure(dpi=1200)
        plt.show()


def calculate_CCI(port_val, window, plot=False):
    port_val['CCI'] = (port_val - port_val.rolling(window=window).mean()) / (0.015 * port_val.rolling(window=window).std())
    if plot:
        plt.subplot(2, 1, 1)
        ax = port_val['JPM'].plot(title='BB', fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")

        plt.subplot(2, 1, 2)
        ax = port_val['CCI'].plot(title='BB', fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        plt.figure(dpi=1200)
        plt.show()


def calculate_TRIX(port_val, window, plot=False):
    port_val = port_val/port_val.iloc[0]
    port_val['ex1'] = port_val['JPM'].ewm(span=window, min_periods=1).mean()
    port_val['ex2'] = port_val['ex1'].ewm(span=window, min_periods=1).mean()
    port_val['ex3'] = port_val['ex2'].ewm(span=window, min_periods=1).mean()

    port_val['trix'] = 10000.0 * (port_val['ex3'].diff() / port_val['ex3'])
    if plot:
        plt.rcParams['axes.grid'] = True
        plt.subplot(2, 1, 1)
        ax = port_val['JPM'].plot(title='Stock Price JPM', fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Normalized Price")

        plt.subplot(2, 1, 2)
        ax = port_val['trix'].plot(title='Trix, Window: 18', fontsize=8, color='orange')
        ax.set_xlabel("Date")
        # plt.show()
        plt.subplots_adjust(hspace=0.9)
        plt.savefig("Trix.jpg", dpi=500)


def calculate_williamsR(port_val, window, plot=False):
    port_val = port_val/port_val.iloc[0]
    max = port_val.rolling(window=window).max()
    min = port_val.rolling(window=window).min()
    port_val['williams'] = 100.0 * (port_val - max) / (max - min)
    if plot:
        plt.rcParams['axes.grid'] = True
        plt.subplot(2, 1, 1)
        ax = port_val['JPM'].plot(title='Stock Price JPM', fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Normalized Price")

        plt.subplot(2, 1, 2)
        ax = port_val['williams'].plot(title='Williams%R Window: 14', fontsize=8, color='green')
        ax.set_xlabel("Date")
        plt.ylim(-110, 10)
        # plt.show()
        plt.subplots_adjust(hspace=0.9)
        plt.savefig("Williams.jpg", dpi=500)

def calculate_MACD(port_val, fast_window, slow_window, signal_window, plot=False):
    # Moving average convergence divergence
    port_val['slow_window'] = port_val['JPM'].ewm(span=slow_window, min_periods=1).mean()
    port_val['fast_window'] = port_val['JPM'].ewm(span=fast_window, min_periods=1).mean()
    port_val['macd'] = port_val['fast_window'] - port_val['slow_window']
    port_val['macdem'] = port_val['macd'].ewm(span=signal_window).mean()
    port_val['macdos'] = port_val['macd'] - port_val['macdem']
    if plot:
        plt.subplot(2, 1, 1)
        ax = port_val['JPM'].plot(title='BB', fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")

        plt.subplot(2, 1, 2)
        ax = port_val[['fast_window', 'slow_window', 'JPM']].plot(title='BB', fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        plt.figure(dpi=1200)
        plt.show()


def calculate_OBV(self, port_val, window, plot=False):
    pass

def all():
    jpm_df = yf.Ticker('JPM')
    port_val = jpm_df.history(period="1Y")[['Close']]
    port_val.rename(columns={'Close': "JPM"}, inplace=True)

    # BB
    calculate_BB(port_val, 20, True)
    # RSI
    calculate_RSI_EMV(port_val, 14, True)
    # Momentum
    calculate_momentum(port_val, 20, True)
    # Williams R
    calculate_williamsR(port_val, 14, True)
    # Trix
    calculate_TRIX(port_val, 18, True)
    # CCI
    calculate_CCI(port_val, 20, True)
    # Z-Score
    calculate_zscore(port_val, 20, True)
    # SMA
    calculate_SMA(port_val, 20, True)
    # MACD
    calculate_MACD(port_val, 12, 26, 9, True)
    # OBV
    calculate_OBV(port_val, 14, True)


if __name__ == '__main__':
    symbols = ["JPM"]
    start_date = "2008-01-01"
    end_date = "2009-12-31"
    port_val = get_data(symbols, pd.date_range(start_date, end_date), addSPY=False)
    print(port_val)
    port_val.fillna(method='ffill', inplace=True)
    # calculate_SMA(port_val, 20, True)
    # calculate_RSI_EMV(port_val, 14, True)
    # calculate_momentum(port_val, 20, True)
    # calculate_williamsR(port_val, 14, True)
    calculate_TRIX(port_val, 18, True)


    # share = [1000, -1000]
    # date = [port_val.index[0], port_val.index[-1]]
    # df_bchm = pd.DataFrame(data=share, index=date, columns=['orders'])
    # print(df_bchm)
    # compute_portvals(df_bchm, start_val=100000, commision=0.0, impact=0.0)

