import streamlit as st
import plotly.graph_objects as go
from utils.data_collector import CryptoDataCollector
from datetime import datetime

st.set_page_config(
    page_title="Bitcoin Mining Analytics",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'data_collector' not in st.session_state:
    st.session_state.data_collector = CryptoDataCollector()
    st.session_state.data_loaded = False

def load_data():
    """Load and prepare data"""
    try:
        if not st.session_state.data_loaded:
            with st.spinner('Loading data...'):
                success = st.session_state.data_collector.collect_all_data()
                if success:
                    st.session_state.data_loaded = True
                    return True
                else:
                    st.error("Failed to load data")
                    return False
        return True
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return False

def main():
    st.title("Bitcoin Mining Analytics Dashboard")
    
    if load_data():
        price_data = st.session_state.data_collector.price_data
        
        # Overview metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Current Bitcoin Price",
                f"${price_data['price'].iloc[-1]:,.2f}"
            )
            
        with col2:
            daily_return = price_data['price'].pct_change().iloc[-1] * 100
            st.metric(
                "24h Change",
                f"{daily_return:.2f}%"
            )
            
        with col3:
            st.metric(
                "30-Day High",
                f"${price_data['price'].max():,.2f}"
            )

        # Price overview chart
        st.subheader("Price Overview")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=price_data['timestamp'],
            y=price_data['price'],
            name='Price',
            line=dict(color='blue')
        ))
        
        fig.update_layout(
            title='Bitcoin Price History (30 Days)',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            height=500,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)

        # Add dashboard description
        st.markdown("""
        ### About This Dashboard
        This Bitcoin Mining Analytics Dashboard provides comprehensive analysis tools:
        
        * **Mining Calculator**: Calculate mining profitability with adjustable parameters
        * **Technical Analysis**: View price trends, RSI, MACD, and Bollinger Bands
        * **Correlation Analysis**: Analyze Bitcoin's correlation with other assets
        
        Use the sidebar to navigate between different analysis tools.
        """)

if __name__ == "__main__":
    main()