import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st  # Added this import

class CryptoDataCollector:
    def __init__(self):
        self.api_key = self.get_api_key()
        if not self.api_key:
            raise ValueError("No API key found")
            
        self.headers = {
            'X-CG-API-KEY': self.api_key
        }
        self.price_data = None
        self.market_data = None

    def get_api_key(self):  # Fixed indentation - was inside __init__
        """Get API key from environment variables or Streamlit secrets"""
        # Try .env file first
        load_dotenv()
        api_key = os.getenv('COINGECKO_API_KEY')
        
        # If not in .env, try Streamlit secrets
        if not api_key and hasattr(st, 'secrets'):
            api_key = st.secrets.get('COINGECKO_API_KEY')
            
        return api_key

    def collect_all_data(self):
        """Collect all necessary data"""
        try:
            self.price_data = self.get_bitcoin_price()
            self.market_data = self.get_bitcoin_market_data()
            return True
        except Exception as e:
            print(f"Error collecting data: {e}")
            return False

    def get_bitcoin_price(self, days=30):
        """Fetch Bitcoin price data from CoinGecko"""
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {
            "vs_currency": "usd",
            "days": str(days),
            "interval": "daily"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Calculate additional metrics
            df['daily_return'] = df['price'].pct_change() * 100
            df['rolling_mean'] = df['price'].rolling(window=7).mean()
            
            return df
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Bitcoin price data: {e}")
            return None

    def get_bitcoin_market_data(self):
        """Fetch current Bitcoin market data"""
        url = "https://api.coingecko.com/api/v3/coins/bitcoin"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            return {
                'current_price_usd': data['market_data']['current_price']['usd'],
                'market_cap_usd': data['market_data']['market_cap']['usd'],
                'total_volume_usd': data['market_data']['total_volume']['usd'],
                'price_change_24h': data['market_data']['price_change_percentage_24h'],
                'last_updated': data['last_updated']
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching market data: {e}")
            return None