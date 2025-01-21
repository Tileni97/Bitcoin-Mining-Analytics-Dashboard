import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="Correlation Analysis", layout="wide")

class CorrelationAnalysis:
    def __init__(self):
        self.asset_mapping = {
            '^GSPC': 'S&P 500',
            'GLD': 'Gold',
            'QQQ': 'NASDAQ',
            'TLT': 'Treasury Bonds'
        }

    def safe_download_data(self, symbol, start_date, end_date, retries=3):
        """Safely download data with retries"""
        for attempt in range(retries):
            try:
                data = yf.download(
                    symbol,
                    start=start_date,
                    end=end_date,
                    progress=False
                )
                if not data.empty and 'Close' in data.columns:
                    return data['Close'].squeeze()
                time.sleep(1)
            except Exception as e:
                if attempt == retries - 1:
                    st.warning(f"Failed to fetch data for {symbol}")
                time.sleep(1)
        return None

    def fetch_market_data(self, start_date, end_date):
        """Fetch data for all assets"""
        assets = {}
        
        with st.spinner('Fetching market data...'):
            # Get Bitcoin data from our collector
            if 'data_collector' in st.session_state:
                bitcoin_data = st.session_state.data_collector.price_data
                bitcoin_returns = pd.Series(
                    bitcoin_data['price'].values,
                    index=bitcoin_data['timestamp'],
                    name='Bitcoin'
                ).pct_change().dropna()
                assets['Bitcoin'] = bitcoin_returns

            # Get other assets
            for symbol, name in self.asset_mapping.items():
                price_data = self.safe_download_data(symbol, start_date, end_date)
                if price_data is not None:
                    assets[name] = price_data.pct_change().dropna()

        return assets if len(assets) > 1 else None

    def calculate_correlations(self, assets_dict):
        """Calculate correlation matrix"""
        returns_data = pd.DataFrame({name: returns for name, returns in assets_dict.items()})
        returns_data = returns_data.fillna(method='ffill').dropna()
        return returns_data.corr()

    def plot_correlation_heatmap(self, corr_matrix):
        """Create correlation heatmap"""
        fig = px.imshow(
            corr_matrix,
            color_continuous_scale='RdBu',
            aspect='auto',
            title='Asset Correlation Matrix'
        )
        
        fig.update_layout(
            width=800,
            height=800,
            title_x=0.5
        )
        
        return fig

    def plot_rolling_correlation(self, df, asset1, asset2, window=30):
        """Create rolling correlation plot"""
        rolling_corr = df[asset1].rolling(window=window).corr(df[asset2])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=rolling_corr.index,
            y=rolling_corr,
            mode='lines',
            name=f'{window}-Day Rolling Correlation'
        ))
        
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        
        fig.update_layout(
            title=f'{window}-Day Rolling Correlation between {asset1} and {asset2}',
            yaxis_title='Correlation Coefficient',
            xaxis_title='Date',
            height=400,
            showlegend=True
        )
        
        return fig

def main():
    st.title('Bitcoin Correlation Analysis')

    if 'data_collector' in st.session_state and st.session_state.data_loaded:
        # Initialize correlation analysis
        correlation = CorrelationAnalysis()
        
        # Date range selection
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=datetime.now() - timedelta(days=30)
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                value=datetime.now()
            )

        if start_date < end_date:
            # Fetch and analyze data
            asset_data = correlation.fetch_market_data(start_date, end_date)
            
            if asset_data:
                # Create combined DataFrame for analysis
                combined_data = pd.DataFrame(asset_data)
                
                # Calculate correlations
                correlation_matrix = correlation.calculate_correlations(asset_data)
                
                # Display correlation heatmap
                st.subheader('Correlation Heatmap')
                st.plotly_chart(correlation.plot_correlation_heatmap(correlation_matrix), 
                              use_container_width=True)
                
                # Rolling correlation analysis
                st.subheader('Rolling Correlation Analysis')
                
                col1, col2 = st.columns(2)
                with col1:
                    window = st.slider('Rolling Window (Days)', 
                                    min_value=7, 
                                    max_value=90, 
                                    value=30)
                
                with col2:
                    selected_asset = st.selectbox(
                        'Select Asset for Rolling Correlation',
                        [asset for asset in asset_data.keys() if asset != 'Bitcoin']
                    )
                
                if selected_asset:
                    st.plotly_chart(correlation.plot_rolling_correlation(
                        combined_data,
                        'Bitcoin',
                        selected_asset,
                        window=window
                    ), use_container_width=True)
                
                # Correlation statistics table
                st.subheader('Correlation Statistics')
                st.dataframe(
                    correlation_matrix.style.format("{:.2f}")
                    .background_gradient(cmap='RdBu', vmin=-1, vmax=1)
                )
                
                # Analysis insights
                st.subheader('Key Insights')
                
                # Calculate metrics
                avg_corr = correlation_matrix['Bitcoin'].drop('Bitcoin').mean()
                max_corr = correlation_matrix['Bitcoin'].drop('Bitcoin').max()
                min_corr = correlation_matrix['Bitcoin'].drop('Bitcoin').min()
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average Correlation", f"{avg_corr:.2f}")
                with col2:
                    st.metric("Strongest Correlation", f"{max_corr:.2f}")
                with col3:
                    st.metric("Weakest Correlation", f"{min_corr:.2f}")
                
                # Educational content
                st.markdown("""
                ### Understanding Correlations
                
                Correlation coefficients range from -1 to +1:
                - **+1.0**: Perfect positive correlation
                - **0.0**: No correlation
                - **-1.0**: Perfect negative correlation
                
                ### Interpreting Results
                - Strong Positive: > 0.5
                - Moderate Positive: 0.3 to 0.5
                - Weak Positive: 0 to 0.3
                - Weak Negative: -0.3 to 0
                - Moderate Negative: -0.5 to -0.3
                - Strong Negative: < -0.5
                
                ### Using This Information
                - **Portfolio Diversification**: Assets with low or negative correlations can help reduce portfolio risk
                - **Market Analysis**: Understanding how Bitcoin moves relative to traditional markets
                - **Risk Management**: Planning for market conditions based on historical relationships
                """)
                
        else:
            st.error("End date must be after start date")
    else:
        st.error("Please load data from the Home page first")

if __name__ == "__main__":
    main()