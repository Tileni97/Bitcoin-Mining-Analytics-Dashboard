import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class MiningDataAnalyzer:
    def __init__(self):
        self.data_dir = Path('data')
        plt.style.use('default')

    def read_data(self):
        """Read and prepare all data"""
        try:
            self.price_data = pd.read_csv(self.data_dir / 'bitcoin_prices.csv')
            self.market_data = pd.read_csv(self.data_dir / 'bitcoin_market_data.csv')
            
            # Convert timestamp to datetime
            self.price_data['timestamp'] = pd.to_datetime(self.price_data['timestamp'])
            
            # Calculate basic metrics
            self.price_data['daily_return'] = self.price_data['price'].pct_change() * 100
            self.price_data['rolling_mean'] = self.price_data['price'].rolling(window=7).mean()
            self.price_data['volatility'] = self.price_data['daily_return'].rolling(window=7).std()
            
            # Calculate technical indicators
            self.calculate_technical_indicators()
            
            return True
        except Exception as e:
            print(f"Error reading data: {e}")
            return False

    def calculate_technical_indicators(self):
        """Calculate technical analysis indicators"""
        df = self.price_data
        
        # RSI
        delta = df['price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        # MACD
        exp1 = df['price'].ewm(span=12, adjust=False).mean()
        exp2 = df['price'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

        # Bollinger Bands
        df['BB_middle'] = df['price'].rolling(window=20).mean()
        bb_std = df['price'].rolling(window=20).std()
        df['BB_upper'] = df['BB_middle'] + (bb_std * 2)
        df['BB_lower'] = df['BB_middle'] - (bb_std * 2)

    def calculate_risk_metrics(self):
        """Calculate risk analysis metrics"""
        returns = self.price_data['daily_return'].dropna()
        
        # Value at Risk (95% confidence)
        var_95 = np.percentile(returns, 5)
        
        # Maximum Drawdown
        cumulative_returns = (1 + returns/100).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdowns = cumulative_returns/rolling_max - 1
        max_drawdown = drawdowns.min() * 100

        # Annualized metrics
        annual_return = returns.mean() * 252
        annual_volatility = returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / annual_volatility if annual_volatility != 0 else 0

        return {
            'Value at Risk (95%)': f"{var_95:.2f}%",
            'Maximum Drawdown': f"{max_drawdown:.2f}%",
            'Annualized Return': f"{annual_return:.2f}%",
            'Annualized Volatility': f"{annual_volatility:.2f}%",
            'Sharpe Ratio': f"{sharpe_ratio:.2f}"
        }

    def calculate_mining_metrics(self):
        """Calculate mining-specific metrics"""
        # Placeholder for mining metrics - to be expanded with real data
        last_price = self.price_data['price'].iloc[-1]
        
        # Example mining calculations
        difficulty = 71.8e6  # Example difficulty
        hashrate = 500e6    # Example hashrate (in TH/s)
        power_cost = 0.12   # Example power cost per kWh
        power_usage = 3000  # Example power usage in watts
        
        # Daily power cost
        daily_power_cost = (power_usage / 1000) * 24 * power_cost
        
        # Estimated daily BTC reward (simplified)
        daily_btc = (hashrate * 86400) / (difficulty * 2**32)
        
        # Daily revenue and profit
        daily_revenue = daily_btc * last_price
        daily_profit = daily_revenue - daily_power_cost

        return {
            'Network Difficulty': f"{difficulty/1e6:.2f}M",
            'Hashrate': f"{hashrate/1e6:.2f} TH/s",
            'Daily Revenue': f"${daily_revenue:.2f}",
            'Daily Power Cost': f"${daily_power_cost:.2f}",
            'Daily Profit': f"${daily_profit:.2f}",
            'Break-even Price': f"${(daily_power_cost/daily_btc):.2f}"
        }

    def create_technical_plots(self, figures_dir):
        """Create technical analysis plots"""
        # RSI Plot
        plt.figure(figsize=(12, 6))
        plt.plot(self.price_data['timestamp'], self.price_data['RSI'])
        plt.axhline(y=70, color='r', linestyle='--')
        plt.axhline(y=30, color='g', linestyle='--')
        plt.title('Relative Strength Index (RSI)')
        plt.grid(True, alpha=0.3)
        plt.savefig(figures_dir / 'rsi.png', dpi=300, bbox_inches='tight')
        plt.close()

        # MACD Plot
        plt.figure(figsize=(12, 6))
        plt.plot(self.price_data['timestamp'], self.price_data['MACD'], label='MACD')
        plt.plot(self.price_data['timestamp'], self.price_data['Signal_Line'], label='Signal Line')
        plt.title('MACD')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(figures_dir / 'macd.png', dpi=300, bbox_inches='tight')
        plt.close()

        # Bollinger Bands
        plt.figure(figsize=(12, 6))
        plt.plot(self.price_data['timestamp'], self.price_data['price'], label='Price')
        plt.plot(self.price_data['timestamp'], self.price_data['BB_upper'], label='Upper Band')
        plt.plot(self.price_data['timestamp'], self.price_data['BB_middle'], label='Middle Band')
        plt.plot(self.price_data['timestamp'], self.price_data['BB_lower'], label='Lower Band')
        plt.title('Bollinger Bands')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(figures_dir / 'bollinger.png', dpi=300, bbox_inches='tight')
        plt.close()

    def create_visualizations(self):
        """Create and save all visualization plots"""
        figures_dir = self.data_dir / 'figures'
        figures_dir.mkdir(exist_ok=True)

        # Original plots
        plt.figure(figsize=(12, 6))
        plt.plot(self.price_data['timestamp'], self.price_data['price'], 'b-', label='Price')
        plt.plot(self.price_data['timestamp'], self.price_data['rolling_mean'], 'r--', label='7-Day MA')
        plt.title('Bitcoin Price and Moving Average')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(figures_dir / 'price_trend.png', dpi=300, bbox_inches='tight')
        plt.close()

        # Returns Distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(self.price_data['daily_return'].dropna(), bins=20)
        plt.title('Distribution of Daily Returns')
        plt.xlabel('Daily Return (%)')
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        plt.savefig(figures_dir / 'returns_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()

        # Technical Analysis plots
        self.create_technical_plots(figures_dir)

    def print_analysis(self):
        """Print comprehensive analysis results"""
        print("\n=== Bitcoin Mining Data Analysis ===")
        print(f"\nAnalysis generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\nTimestamp Range:")
        print(f"From: {self.price_data['timestamp'].min()}")
        print(f"To: {self.price_data['timestamp'].max()}")

        # Basic stats
        price_stats = {
            'Price Statistics': {
                'Current Price': f"${self.price_data['price'].iloc[-1]:.2f}",
                'Average Price': f"${self.price_data['price'].mean():.2f}",
                'Highest Price': f"${self.price_data['price'].max():.2f}",
                'Lowest Price': f"${self.price_data['price'].min():.2f}",
                'Price Volatility': f"${self.price_data['price'].std():.2f}",
                '7-Day Rolling Volatility': f"{self.price_data['volatility'].iloc[-1]:.2f}%"
            }
        }

        # Print all statistics
        for category, metrics in price_stats.items():
            print(f"\n{category}:")
            for metric, value in metrics.items():
                print(f"{metric}: {value}")

        # Print risk metrics
        print("\nRisk Metrics:")
        risk_metrics = self.calculate_risk_metrics()
        for metric, value in risk_metrics.items():
            print(f"{metric}: {value}")

        # Print mining metrics
        print("\nMining Metrics:")
        mining_metrics = self.calculate_mining_metrics()
        for metric, value in mining_metrics.items():
            print(f"{metric}: {value}")

def main():
    """Main function to run the analysis"""
    analyzer = MiningDataAnalyzer()
    
    if analyzer.read_data():
        analyzer.create_visualizations()
        analyzer.print_analysis()
        print("\nVisualization plots have been saved in the 'data/figures' directory.")
    else:
        print("Could not perform analysis due to data reading error")

if __name__ == "__main__":
    main()