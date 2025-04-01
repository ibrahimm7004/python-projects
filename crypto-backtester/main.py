import pandas as pd
import numpy as np
import datetime
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

        self.calculate_additional_metrics()  # Calculate additional metrics
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
            open_time = pd.to_datetime(row['open_time'], format='%Y-%m-%d %H:%M:%S')
            if open_time < datetime.datetime.now():
                self.position = 'long'
                self.entry_time = open_time
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
        exit_time = row['close_time']  # Replace with the correct column name
        holding_time = pd.to_datetime(exit_time) - pd.to_datetime(self.entry_time)
        trade_return = (row['Close'] - row['Open']) / row['Open']
        
        # Update the 'stats' dictionary with the calculated statistics
        self.stats['Avg Position Holding Time'] = holding_time
        self.stats['Avg Trade Return'] = trade_return

    def calculate_additional_metrics(self):
        # Calculate additional metrics
        trades = []  # Placeholder for trades
        max_drawdown = 10  # Placeholder for max drawdown
        max_drawdown_duration = 20  # Placeholder for max drawdown duration
        
        # Perform necessary calculations for trades, max_drawdown, and max_drawdown_duration
        
        self.stats['Start Date'] = self.data.iloc[0]['open_time']
        self.stats['End Date'] = self.data.iloc[-1]['open_time']
        self.stats['Capital Final ($)'] = self.capital
        self.stats['Buy and Hold Return (%)'] = (self.data.iloc[-1]['Close'] - self.data.iloc[0]['Close']) / self.data.iloc[0]['Close'] * 100
        self.stats['Max Drawdown (%)'] = max_drawdown * 100
        self.stats['Max Drawdown Duration'] = max_drawdown_duration
        self.stats['No. of Trades Taken'] = len(trades)
        if len(trades) > 0:
            self.stats['Win Rate (%)'] = sum([1 for trade_return in trades if trade_return > 0]) / len(trades) * 100
        else:
            self.stats['Win Rate (%)'] = 0
        if len(trades) > 0:
            self.stats['Worst Trade (%)'] = min(trades) * 100
        else:
            self.stats['Worst Trade (%)'] = 0
        if len(trades) > 0:
            self.stats['Best Trade (%)'] = max(trades) * 100
        else:
            self.stats['Best Trade (%)'] = 0
        self.stats['Avg Trade Return (%)'] = np.mean(trades) * 100

        # Calculate Sortino Ratio
        return_rate = 0.08  # Example return rate
        risk_free_rate = 0.02  # Example risk-free rate
        negative_returns = [-0.05, -0.03, -0.02, -0.01]  # Example negative returns as a list
        downside_returns = np.minimum(negative_returns, 0)  # Extract negative returns
        downside_deviation = np.std(downside_returns)  # Calculate standard deviation of negative returns
        self.stats['Sortino Ratio'] = (return_rate - risk_free_rate) / downside_deviation

        # Calculate Calmar Ratio
        average_annual_return = 3000000
        self.stats['Calmar Ratio'] = average_annual_return / max_drawdown
    
        # Calculate Sharpe ratio
        risk_free_rate = 0.01  # Assuming 1% annual risk-free rate
        returns = [(trade_return + 1) for trade_return in trades]
        cumulative_returns = np.cumprod(returns)
        daily_returns = (cumulative_returns[1:] / cumulative_returns[:-1]) - 1
        daily_returns = np.insert(daily_returns, 0, 0)  # Insert 0 as the first element for the first day
        risk_adjusted_returns = daily_returns - risk_free_rate / 252  # Adjusting for daily risk-free rate
        self.stats['Sharpe Ratio'] = np.mean(risk_adjusted_returns) / np.std(risk_adjusted_returns)
        
        # Calculate Expectancy
        win_rate = 0.6  # Example win rate (60%)
        average_win_size = 1000  # Example average win size
        loss_rate = 0.4  # Example loss rate (40%)
        average_loss_size = 500  # Example average loss size
        self.stats['Expectancy'] = (win_rate * average_win_size) - (loss_rate * average_loss_size)

        # Calculate SQN using R-Expectancy
        r_expectancy = [0.5, 0.3, 0.4, 0.2, 0.1]  # Example R-expectancy values
        trades = len(r_expectancy)  # Example number of trades
        r_expectancy_std = np.std(r_expectancy)
        self.stats['SQN'] = np.mean(r_expectancy) / r_expectancy_std * np.sqrt(trades)


    def print_statistics(self):
        # Print the calculated metrics
        print("Backtest Statistics:")
        print("==========================")
        print("Sharpe Ratio:", "{:.2f}".format(self.stats['Sharpe Ratio']))
        print("Sortino Ratio:", "{:.2f}".format(self.stats['Sortino Ratio']))
        print("Calmar Ratio:", "{:.2f}".format(self.stats['Calmar Ratio']))
        print("Avg Position Holding Time:", self.stats['Avg Position Holding Time'])
        print("Max Drawdown (% of capital):", "{:.2f}%".format(self.stats['Max Drawdown (%)']))
        print("SQN:", "{:.2f}".format(self.stats['SQN']))
        print("Start Date:", self.stats['Start Date'])
        print("End Date:", self.stats['End Date'])
        print("Capital Final ($):", "{:.2f}".format(self.stats['Capital Final ($)']))
        print("Buy and Hold Return (%):", "{:.2f}%".format(self.stats['Buy and Hold Return (%)']))
        print("Max DD Duration:", self.stats['Max Drawdown Duration'])
        print("No. of Trades Taken:", self.stats['No. of Trades Taken'])
        print("Win Rate (%):", "{:.2f}%".format(self.stats['Win Rate (%)']))
        print("Worst Trade (%):", "{:.2f}%".format(self.stats['Worst Trade (%)']))
        print("Best Trade (%):", "{:.2f}%".format(self.stats['Best Trade (%)']))
        print("Avg Trade Return (%):", "{:.2f}%".format(self.stats['Avg Trade Return (%)']))
        print("Expectancy:", "{:.2f}".format(self.stats['Expectancy']))
        print("==========================")

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
