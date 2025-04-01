import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime


class backtester:
    def __init__(self, starting_capital, sl_limit, dl_limit, file_name):
        self.data = pd.read_csv(file_name)
        self.sl_limit = sl_limit
        self.dl_limit = dl_limit
        self.starting_capital = starting_capital
        self.capital = self.starting_capital
        self.num_of_trades = 0
        self.position = None
        self.long_timestamps = []  # List to store long entry timestamps

    def backtest(self):
        for row in self.data.iterrows():
            self.calc_stop_loss()
            if self.position != 'stop':
                self.calc_daily_loss()
                if self.position != 'pause':
                    self.check_entry_conditions(row)
                    self.check_exit_conditions(row)
        return self.num_of_trades

    def calc_daily_loss(self):
        daily_limit = self.starting_capital * self.dl_limit
        if self.capital - self.starting_capital <= daily_limit:
            self.position = 'pause'

    def calc_stop_loss(self):
        daily_limit = self.starting_capital * self.sl_limit
        if self.capital - self.starting_capital <= daily_limit:
            self.position = 'stop'

    def check_entry_conditions(self, row):
        open_time = pd.to_datetime(
            row[1]['open_time'], format='%Y-%m-%d %H:%M:%S')
        if row[1]['typical_price'] < row[1]['vwap_lowerband1']:
            if self.position != 'long':
                self.position = 'long'
                self.num_of_trades += 1
                self.entry_time = open_time
                # Append the long entry timestamp
                self.long_timestamps.append(open_time)
                self.calculate_position_size(row)
                self.calculate_transaction_fee(row)

    def check_exit_conditions(self, row):
        open_time = pd.to_datetime(
            row[1]['open_time'], format='%Y-%m-%d %H:%M:%S')
        if row[1]['typical_price'] > row[1]['vwap_upperband1']:
            if self.position != 'short':
                self.position = 'short'
                self.num_of_trades += 1
                self.entry_time = open_time
                self.calculate_position_size(row)
                self.calculate_transaction_fee(row)

    def calculate_position_size(self, row):
        risk_per_trade = 0.01 * self.capital
        lev = 10
        entry_price = row[1]['Open']
        sl_price = row[1]['Close'] - 2 * row[1]['ATR']
        distance_to_sl = (entry_price - sl_price) / entry_price
        position_size = float(
            np.floor(risk_per_trade / (distance_to_sl * entry_price)))
        position_size_limit = 0.4 * self.capital
        position_size = min(position_size, position_size_limit)
        self.position_size = position_size

    def calculate_transaction_fee(self, row):
        # Assuming a simple transaction fee calculation based on a fixed fee per trade:
        # Modify this function according to the fee structure of your exchange or broker
        fee_rate = 0.02  # 0.2% fee rate
        # Calculate the transaction fee based on the position size
        transaction_fee = self.position_size * \
            row[1]['typical_price'] * fee_rate
        # Deduct the transaction fee from the capital
        self.capital -= transaction_fee
        # Keeping track of total transaction fees incurred
        self.total_transaction_fees += transaction_fee

    def plot_capital_chart(self):
        dates = []
        capital_percentage = []

        for row in self.data.iterrows():
            # Append date to the list of dates
            dates.append(pd.to_datetime(
                row[1]['open_time'], format='%Y-%m-%d %H:%M:%S'))
            # Calculate the percentage growth of capital over time and append to the list of capital percentages
            capital_growth = (
                row[1]['typical_price'] - self.starting_capital) / self.starting_capital * 100
            capital_percentage.append(capital_growth)

        fig = go.Figure(data=go.Scatter(
            x=dates, y=capital_percentage, mode='lines'))
        fig.update_layout(title='Capital Growth',
                          xaxis_title='Time', yaxis_title='Capital Percentage')
        fig.show()


file_name = 'data.csv'

starting_capital = float(input("Input Starting Capital: "))
sl_limit = float(input("Input SL Limit: "))
dl_limit = float(input("Input Daily Loss Limit: "))

bt = backtester(starting_capital, sl_limit, dl_limit, file_name)
trades = bt.backtest()
print("Num of Trades Made: ", trades)
bt.plot_capital_chart()
