import pandas as pd
import numpy as np
import plotly.graph_objects as go

class Backtester:
    def __init__(self, data_file, starting_capital):
        self.data = pd.read_csv(data_file)
        self.starting_capital = starting_capital
        self.capital = starting_capital
        self.position = None
        self.entry_time = None
        self.stats = {}  # Store metrics
    
    def backtest(self):
        # Perform the backtesting process
        self.calculate_indicators()  # Calculate any indicators needed
        for i, row in self.data.iterrows():
            self.check_stop_loss_limit()  # Check if daily max % loss limit is reached
            self.check_entry_conditions(row)  # Check entry conditions for a new position
            self.check_exit_conditions(row)  # Check exit conditions for the current position
        
        self.print_statistics()  # Print backtest statistics
        self.plot_capital_chart()  # Plot the capital growth chart
    
    def calculate_indicators(self):
        # Calculate any indicators you need for backtesting
        # For example, calculate vwap_lowerband1, vwap_upperband1, ATR
        self.data['vwap_lowerband1'] = self.data['vwap'] - self.data['vwap_stdev']
        self.data['vwap_upperband1'] = self.data['vwap'] + self.data['vwap_stdev']

    def check_stop_loss_limit(self):
        # Check if daily max % loss limit is reached
        # If reached, stop trading for the day and close any open position
        # Adjust the code as needed based on your data structure and column names
        daily_max_loss_limit = self.starting_capital * 0.02  # 2% daily loss limit
        if self.capital - self.starting_capital <= -daily_max_loss_limit:
            self.position = None
    
    def check_entry_conditions(self, row):
        # Check if there is no current position
        if self.position is None:
            # Check if price drops below vwap_lowerband1, go long
            if row['Low'] < row['vwap_lowerband1']:
                self.position = 'long'
                self.entry_time = row['open_time']
                self.calculate_position_size(row)  # Calculate position size
                self.calculate_transaction_fee(row)  # Calculate transaction fee
    
    def check_exit_conditions(self, row):
        # Check if there is a long position
        if self.position == 'long':
            # Implement TP/SL mechanism, trailing stop loss, and transaction fee
            tp_price = row['Close'] + 2 * row['ATR']  # Example TP price: Close price + 2 * ATR
            sl_price = row['Close'] - 2 * row['ATR']  # Example SL price: Close price - 2 * ATR
            
            # Check if the price reaches the TP or SL levels
            if row['High'] >= tp_price or row['Low'] <= sl_price:
                self.position = None  # Close the position
                self.calculate_exit_statistics(row)  # Calculate exit statistics
    
    def calculate_position_size(self, row):
        # Calculate position size based on risk per trade % of capital
        risk_per_trade = 0.01 * self.capital  # change the % risk here per trade, now it's 1%
        lev = 10  # define leverage, more lev means less margin required & vice versa
        entry_price = row['Open']  # Assuming 'Open' column contains the entry price
        sl_price = row['Close'] - 2 * row['ATR']  # Example SL price: Close price - 2 * ATR
        
        # Calculate relative % distance to SL (will be in decimal %, like 0.01 aka 1%)
        distance_to_sl = (entry_price - sl_price) / entry_price
        
        # Calculate position size, which we will put in the size param for long
        position_size = float(np.floor(risk_per_trade / (distance_to_sl * entry_price)))
        
        # Position size limit set as a fraction of equity
        position_size_limit = 0.4 * self.capital
        position_size = min(position_size, position_size_limit)
        
        self.position_size = position_size  # Update the position size attribute
        
    def calculate_transaction_fee(self, row):
        # Calculate transaction fee based on the position size and a fixed fee rate
        fee_rate = 0.001  # 0.1% fee rate
        self.transaction_fee = fee_rate * self.position_size * row['Close']
        self.capital -= self.transaction_fee
    
    def calculate_exit_statistics(self, row):
        # Calculate and store exit statistics such as trade return, holding time, etc.
        exit_time = row['open_time']
        holding_time = pd.to_datetime(exit_time) - pd.to_datetime(self.entry_time)
        trade_return = (row['Close'] - row['Open']) / row['Open']
        
        # Update the 'stats' dictionary with the calculated statistics
        self.stats['Avg Position Holding Time'] = holding_time
        self.stats['Avg Trade Return'] = trade_return
    
    def print_statistics(self):
        # Calculate and print metrics such as Sharpe ratio, Cortino ratio, etc.
        # You can use the stored exit statistics to calculate these metrics
        print("Backtest Statistics:")
        print("Avg Position Holding Time:", self.stats['Avg Position Holding Time'])
        print("Avg Trade Return:", self.stats['Avg Trade Return'])
    
    def plot_capital_chart(self):
        # Plot the capital growth chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.data['open_time'], y=[self.starting_capital] * len(self.data),
                                 mode='lines', name='Starting Capital'))
        fig.add_trace(go.Scatter(x=self.data['open_time'], y=self.data['Close'] * self.position_size,
                                 mode='lines', name='Capital'))
        
        fig.update_layout(title='Backtest Capital Growth', xaxis_title='Date', yaxis_title='Capital')
        fig.show()


# Usage
backtester = Backtester('C:/Users/hp/Downloads/data.csv', starting_capital=10000)
backtester.backtest()