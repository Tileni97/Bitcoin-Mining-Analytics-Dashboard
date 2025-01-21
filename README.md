# Bitcoin Mining Analytics Dashboard

A real-time analytics platform for Bitcoin mining analysis, combining profitability calculations, technical indicators, and market correlation insights. Built with Python and Streamlit, this dashboard provides comprehensive tools for mining profitability assessment and market analysis.

![Dashboard Preview](screens/Screenshot%202025-01-21%20222406.png)
![Dashboard Preview](screens/Screenshot%202025-01-21%20222459.png)

## Features

### 💹 Mining Profitability Calculator
- Real-time profitability calculations
- Adjustable parameters (hashrate, power consumption, electricity costs)
- ROI and break-even analysis
- Profit projection charts

### 📊 Technical Analysis
- Real-time price tracking
- Multiple technical indicators:
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
- Interactive charts and visualizations

### 🔄 Market Correlation Analysis
- Bitcoin correlation with traditional assets
- Rolling correlation calculations
- Interactive heatmaps
- Advanced statistical metrics

## Technology Stack

- **Backend**: Python
- **Frontend**: Streamlit
- **Data Sources**: 
  - CoinGecko API
  - Yahoo Finance API
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Plotly

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bitcoin-mining-analytics.git
cd bitcoin-mining-analytics
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory:
```
COINGECKO_API_KEY=your_api_key_here
```

5. Run the dashboard:
```bash
streamlit run src/Home.py
```

## Project Structure

```
mining-dashboard/
├── src/
│   ├── pages/              # Dashboard pages
│   │   ├── mining_calculator.py
│   │   ├── technical_analysis.py
│   │   └── correlation_analysis.py
│   ├── utils/              # Utility functions
│   │   ├── data_collector.py
│   │   └── data_analyzer.py
│   └── Home.py            # Main dashboard
├── data/                  # Data storage
├── requirements.txt       # Dependencies
└── README.md
```

## Usage

1. **Mining Calculator**:
   - Input your mining parameters
   - View profitability metrics
   - Analyze break-even scenarios

2. **Technical Analysis**:
   - Monitor price trends
   - Track technical indicators
   - Identify trading signals

3. **Correlation Analysis**:
   - Compare Bitcoin with traditional assets
   - View correlation heatmaps
   - Analyze market relationships

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CoinGecko API](https://www.coingecko.com/en/api) for cryptocurrency data
- [Yahoo Finance API](https://finance.yahoo.com/) for market data
- [Streamlit](https://streamlit.io/) for the web interface

## Contact

Your Name - tilenihango@gmail.com

Project Link: [https://github.com/Tileni97/Bitcoin-Mining-Analytics-Dashboard](https://github.com/Tileni97/Bitcoin-Mining-Analytics-Dashboard)