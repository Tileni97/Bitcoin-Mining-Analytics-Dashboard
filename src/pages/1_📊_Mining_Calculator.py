import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Mining Calculator", layout="wide")

class MiningCalculator:
    def __init__(self):
        self.default_params = {
            'hashrate': 500,  # TH/s
            'power_consumption': 3000,  # Watts
            'power_cost': 0.12,  # USD per kWh
            'pool_fee': 2,  # Percentage
            'hardware_cost': 10000,  # USD
            'difficulty': 71.8e6
        }

    def calculate_profitability(self, btc_price, params):
        """Calculate mining profitability"""
        # Daily BTC reward calculation
        daily_btc = (params['hashrate'] * 1e12 * 86400) / (params['difficulty'] * 2**32)
        
        # Revenue calculations
        daily_revenue = daily_btc * btc_price
        pool_fee_cost = daily_revenue * (params['pool_fee'] / 100)
        
        # Power cost calculation
        daily_power_cost = (params['power_consumption'] / 1000) * 24 * params['power_cost']
        
        # Profit calculations
        daily_profit = daily_revenue - daily_power_cost - pool_fee_cost
        monthly_profit = daily_profit * 30
        yearly_profit = daily_profit * 365
        
        # ROI calculation
        roi_days = params['hardware_cost'] / daily_profit if daily_profit > 0 else float('inf')
        
        return {
            'Daily BTC': daily_btc,
            'Daily Revenue': daily_revenue,
            'Daily Power Cost': daily_power_cost,
            'Daily Profit': daily_profit,
            'Monthly Profit': monthly_profit,
            'Yearly Profit': yearly_profit,
            'ROI Days': roi_days,
            'Break-even Price': daily_power_cost/daily_btc if daily_btc > 0 else float('inf')
        }

    def plot_profitability_chart(self, params):
        """Create profitability analysis chart"""
        prices = range(20000, 100000, 5000)
        profits = [self.calculate_profitability(price, params)['Daily Profit'] 
                  for price in prices]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=list(prices),
            y=profits,
            mode='lines+markers',
            name='Daily Profit'
        ))
        
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        
        fig.update_layout(
            title='Daily Mining Profit vs Bitcoin Price',
            xaxis_title='Bitcoin Price ($)',
            yaxis_title='Daily Profit ($)',
            height=500,
            showlegend=True
        )
        
        return fig

def main():
    st.title('Bitcoin Mining Profitability Calculator')
    
    calculator = MiningCalculator()
    
    # Sidebar inputs
    st.sidebar.header('Mining Parameters')
    params = calculator.default_params.copy()
    
    params['hashrate'] = st.sidebar.slider(
        'Hashrate (TH/s)', 
        min_value=100, 
        max_value=2000, 
        value=500,
        step=100
    )
    
    params['power_consumption'] = st.sidebar.slider(
        'Power Consumption (W)', 
        min_value=1000, 
        max_value=5000, 
        value=3000,
        step=100
    )
    
    params['power_cost'] = st.sidebar.slider(
        'Electricity Cost ($/kWh)', 
        min_value=0.01, 
        max_value=0.30, 
        value=0.12,
        step=0.01
    )
    
    params['hardware_cost'] = st.sidebar.number_input(
        'Hardware Cost ($)', 
        min_value=1000, 
        max_value=100000, 
        value=10000,
        step=1000
    )
    
    # Current BTC price input
    current_price = 45000.0  # Default price
    if 'data_collector' in st.session_state and st.session_state.data_loaded:
        current_price = st.session_state.data_collector.price_data['price'].iloc[-1]
    
    btc_price = st.number_input(
        'Current Bitcoin Price ($)', 
        value=current_price, 
        step=100.0
    )
    
    # Calculate profits
    profits = calculator.calculate_profitability(btc_price, params)
    
    # Display results in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Daily Bitcoin Mined", f"{profits['Daily BTC']:.8f} BTC")
        st.metric("Daily Revenue", f"${profits['Daily Revenue']:.2f}")
        st.metric("Daily Profit", f"${profits['Daily Profit']:.2f}")
        
    with col2:
        st.metric("Monthly Profit", f"${profits['Monthly Profit']:.2f}")
        st.metric("Yearly Profit", f"${profits['Yearly Profit']:.2f}")
        st.metric("Break-even Price", f"${profits['Break-even Price']:.2f}")
        
    with col3:
        st.metric("Daily Power Cost", f"${profits['Daily Power Cost']:.2f}")
        st.metric("ROI Period", f"{profits['ROI Days']:.1f} days")
        profit_margin = (profits['Daily Profit'] / profits['Daily Revenue']) * 100
        st.metric("Profit Margin", f"{profit_margin:.1f}%")
    
    # Profitability Chart
    st.subheader('Profitability Analysis')
    st.plotly_chart(calculator.plot_profitability_chart(params), use_container_width=True)
    
    # Add educational content
    st.markdown("""
    ### Understanding the Metrics
    
    - **Daily Bitcoin Mined**: Expected BTC earnings per day
    - **Break-even Price**: Minimum BTC price needed for profitability
    - **ROI Period**: Days until hardware cost is recovered
    - **Profit Margin**: Percentage of revenue that is profit
    
    ### Key Factors Affecting Profitability
    
    1. **Bitcoin Price**: Direct impact on revenue
    2. **Electricity Cost**: Major operational expense
    3. **Hardware Efficiency**: Affects power consumption and hash rate
    4. **Network Difficulty**: Adjusts every 2016 blocks
    """)

if __name__ == "__main__":
    main()