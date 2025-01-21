import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

st.set_page_config(page_title="Technical Analysis", layout="wide")

class TechnicalAnalysis:
    @staticmethod
    def calculate_rsi(data, periods=14):
        """Calculate Relative Strength Index"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def calculate_macd(data, fast=12, slow=26, signal=9):
        """Calculate MACD and Signal Line"""
        exp1 = data.ewm(span=fast, adjust=False).mean()
        exp2 = data.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        return macd, signal_line

    @staticmethod
    def calculate_bollinger_bands(data, window=20, num_std=2):
        """Calculate Bollinger Bands"""
        middle_band = data.rolling(window=window).mean()
        std_dev = data.rolling(window=window).std()
        upper_band = middle_band + (std_dev * num_std)
        lower_band = middle_band - (std_dev * num_std)
        return middle_band, upper_band, lower_band

    def create_candlestick_chart(self, df):
        """Create candlestick chart with volume"""
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                           vertical_spacing=0.03, row_heights=[0.7, 0.3])

        # Price line
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['price'],
            name='Price',
            line=dict(color='blue')
        ), row=1, col=1)

        # Add volume if available
        if 'volume' in df.columns:
            fig.add_trace(go.Bar(
                x=df.index,
                y=df['volume'],
                name='Volume',
                marker_color='gray'
            ), row=2, col=1)

        fig.update_layout(
            title='Bitcoin Price and Volume',
            yaxis_title='Price (USD)',
            yaxis2_title='Volume',
            height=600
        )

        return fig

    def create_rsi_chart(self, df):
        """Create RSI chart"""
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['RSI'],
            name='RSI',
            line=dict(color='purple')
        ))

        # Add overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red")
        fig.add_hline(y=30, line_dash="dash", line_color="green")

        fig.update_layout(
            title='Relative Strength Index (RSI)',
            yaxis_title='RSI Value',
            height=400
        )

        return fig

    def create_macd_chart(self, df):
        """Create MACD chart"""
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                           vertical_spacing=0.03, row_heights=[0.7, 0.3])

        # MACD
        fig.add_trace(
            go.Scatter(x=df.index, y=df['MACD'],
                      name='MACD', line=dict(color='blue')),
            row=1, col=1
        )

        # Signal line
        fig.add_trace(
            go.Scatter(x=df.index, y=df['Signal_Line'],
                      name='Signal Line', line=dict(color='orange')),
            row=1, col=1
        )

        # MACD Histogram
        fig.add_trace(
            go.Bar(x=df.index, y=df['MACD'] - df['Signal_Line'],
                  name='MACD Histogram'),
            row=2, col=1
        )

        fig.update_layout(
            title='MACD Indicator',
            height=500
        )

        return fig

    def create_bollinger_bands_chart(self, df):
        """Create Bollinger Bands chart"""
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['price'],
            name='Price',
            line=dict(color='blue')
        ))

        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['BB_upper'],
            name='Upper Band',
            line=dict(color='gray', dash='dash')
        ))

        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['BB_lower'],
            name='Lower Band',
            line=dict(color='gray', dash='dash'),
            fill='tonexty'
        ))

        fig.update_layout(
            title='Bollinger Bands',
            yaxis_title='Price (USD)',
            height=500
        )

        return fig

def main():
    st.title('Bitcoin Technical Analysis')

    if 'data_collector' in st.session_state and st.session_state.data_loaded:
        # Get data and calculate indicators
        df = st.session_state.data_collector.price_data.copy()
        df.set_index('timestamp', inplace=True)
        
        # Calculate indicators
        df['RSI'] = TechnicalAnalysis.calculate_rsi(df['price'])
        df['MACD'], df['Signal_Line'] = TechnicalAnalysis.calculate_macd(df['price'])
        df['BB_middle'], df['BB_upper'], df['BB_lower'] = TechnicalAnalysis.calculate_bollinger_bands(df['price'])

        # Create analysis instance
        analysis = TechnicalAnalysis()

        # Create tabs for different indicators
        tab1, tab2, tab3, tab4 = st.tabs([
            'Price Overview', 'RSI', 'MACD', 'Bollinger Bands'
        ])

        with tab1:
            st.plotly_chart(analysis.create_candlestick_chart(df), use_container_width=True)
            st.markdown("""
            ### Price Overview
            The price chart shows Bitcoin's price movement over time. Key patterns to look for:
            - Trends (upward, downward, sideways)
            - Support and resistance levels
            - Chart patterns (e.g., head and shoulders, triangles)
            """)

        with tab2:
            st.plotly_chart(analysis.create_rsi_chart(df), use_container_width=True)
            st.markdown("""
            ### RSI (Relative Strength Index)
            RSI measures momentum and can indicate overbought or oversold conditions:
            - Above 70: Potentially overbought
            - Below 30: Potentially oversold
            - Trend strength increases as RSI moves to extremes
            """)

        with tab3:
            st.plotly_chart(analysis.create_macd_chart(df), use_container_width=True)
            st.markdown("""
            ### MACD (Moving Average Convergence Divergence)
            MACD helps identify trend changes and momentum:
            - MACD crossing above Signal Line: Bullish signal
            - MACD crossing below Signal Line: Bearish signal
            - Histogram shows momentum strength
            """)

        with tab4:
            st.plotly_chart(analysis.create_bollinger_bands_chart(df), use_container_width=True)
            st.markdown("""
            ### Bollinger Bands
            Bollinger Bands show volatility and potential price levels:
            - Price near upper band: Potentially overbought
            - Price near lower band: Potentially oversold
            - Band width indicates volatility
            - Price tends to return to the middle band
            """)

    else:
        st.error("Please load data from the Home page first")

if __name__ == "__main__":
    main()