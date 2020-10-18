import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

class Indicators(object):
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

    def __init(self):
        pass

    def author(self):
        return "nitarora"

    def calculate_SMA(self, port_val, window, plot=False):
        port_val["JPM_SMA"] = port_val['JPM'].rolling(window=window).mean()
        if plot:
            ax = port_val.plot(title='SMA', fontsize=8)
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            plt.show()

    def calculate_BB(self, port_val, window, plot=False):
        port_val["JPM_SMA"] = port_val['JPM'].rolling(window=window).mean()
        std = port_val['JPM'].rolling(window=window).std()
        port_val["JPM_BB_U"] = port_val['JPM_SMA'] + 2 * std
        port_val["JPM_BB_L"] = port_val['JPM_SMA'] - 2 * std
        if plot:
            ax = port_val.plot(title='BB', fontsize=8)
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            plt.show()

    def calculate_momentum(self, port_val, window, plot=False):
        port_val['momentum'] = (port_val/port_val.shift(window)) - 1
        if plot:
            plt.subplot(2, 1, 1)
            ax = port_val['JPM'].plot(title='BB', fontsize=8)
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")

            plt.subplot(2, 1, 2)
            ax = port_val['momentum'].plot(title='BB', fontsize=8)
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            plt.figure(dpi=1200)
            plt.show()

    def calculate_RSI_EMV(self, port_val, window, plot=False):
        diff = port_val.dropna().diff()
        diff = diff[1:]

        up_diff, down_diff = diff.copy(), diff.copy()

        up_diff[up_diff < 0] = 0
        down_diff[down_diff > 0] = 0

        total_average_gain = up_diff.ewm(span=window).mean()
        total_average_loss = down_diff.abs().ewm(span=window).mean()

        rs_emv = abs(total_average_gain / total_average_loss)

        rsi_emv = 100.0 - 100.0 / (1.0 + rs_emv)
        port_val['RSI_EMV'] = rsi_emv

        if plot:
            plt.subplot(2, 1, 1)
            ax = port_val['JPM'].plot(title='BB', fontsize=8)
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")

            plt.subplot(2, 1, 2)
            ax = port_val['RSI_EMV'].plot(title='BB', fontsize=8)
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            plt.show()

    def calculate_RSI_SMA(self, port_val, window, plot=False):
        diff = port_val.dropna().diff()
        diff = diff[1:]

        up_diff, down_diff = diff.copy(), diff.copy()

        up_diff[up_diff < 0] = 0
        down_diff[down_diff > 0] = 0

        total_average_gain = up_diff.rolling(window=window).mean()
        total_average_loss = down_diff.abs().rolling(window=window).mean()

        rs_sma = abs(total_average_gain / total_average_loss)

        rsi1 = 100.0 - 100.0 / (1.0 + rs_sma)
        port_val['RSI_SMA'] = rsi1

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

    def calculate_zscore(self, port_val, window,  plot=False):
        port_val['zscore'] = (port_val - port_val.rolling(window=window).mean())/port_val.rolling(window=window).std()
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

    def calculate_OBV(self):
        pass

    def calculate_CCI(self, port_val, window, plot=False):
        port_val['CCI'] =  (port_val - port_val.rolling(window=window).mean()) / (0.015 * port_val.rolling(window=window).std())
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

    def calculate_MACD(self, port_val, fast_window, slow_window, signal_window, plot=False):
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
            ax = port_val[['fast_window', 'slow_window' ,'JPM']].plot(title='BB', fontsize=8)
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            plt.figure(dpi=1200)
            plt.show()

    def calculate_TRIX(self, port_val, window, plot=False):
        port_val['ex1'] = port_val['JPM'].ewm(span=window, min_periods=1).mean()
        port_val['ex2'] = port_val['ex1'].ewm(span=window, min_periods=1).mean()
        port_val['ex3'] = port_val['ex2'].ewm(span=window, min_periods=1).mean()

        port_val['trix'] = 10000 * (port_val['ex3'].diff() / port_val['ex3'])
        if plot:
            plt.subplot(2, 1, 1)
            ax = port_val['JPM'].plot(title='BB', fontsize=8)
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")

            plt.subplot(2, 1, 2)
            ax = port_val['trix'].plot(title='BB', fontsize=8)
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            plt.figure(dpi=1200)
            plt.grid()
            plt.show()

    def calculate_williamsR(self, port_val, window, plot=False):
        max = port_val.rolling(window=window).max()
        min = port_val.rolling(window=window).min()
        port_val['williams'] = 100.0 * (port_val - max) / (max - min)
        if plot:
            plt.subplot(2, 1, 1)
            ax = port_val['JPM'].plot(title='JPM', fontsize=8)
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")

            plt.subplot(2, 1, 2)
            ax = port_val['williams'].plot(title='williams', fontsize=8)
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            plt.ylim(-110, 10)
            plt.figure(dpi=1200)
            plt.show()





if __name__ == '__main__':
    jpm_df = yf.Ticker('JPM')
    port_val = jpm_df.history(period="1Y")[['Close']]
    port_val.rename(columns={'Close': "JPM"}, inplace=True)

    # Indicators().calculate_MACD(port_val, 12, 26, 9, True)
    # Indicators().calculate_RSI_SMA(port_val, 14, True)
    Indicators().calculate_TRIX(port_val, 18, True)
    # Indicators().calculate_zscore(port_val, 20, True)
    # Indicators().calculate_CCI(port_val, 20, True)
    # Indicators().calculate_williamsR(port_val, 14, True)
    # symbols = ["JPM"]
    # start_date = "2008-01-01"
    # end_date = "2009-12-31"
    # port_val = get_data(symbols, pd.date_range(start_date, end_date), addSPY=False)
    # print(port_val)
    # port_val.dropna(inplace=True)
    # port_val.fillna(method='ffill', inplace=True)


    # BB
    # RSI
    # Momentum
    # MACD
    # OBV
