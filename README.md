# QuantResearch - Quant Analyst System for IDX Trading

Multi-layer quantitative trading system for institutional momentum detection in Indonesian stock market (IDX).

## 🎯 Project Overview

Building a comprehensive quant analyst system with:
- **Market Data Collection**: Real-time marketcap from yfinance
- **ML Training**: XGBoost model for trading signal generation
- **Performance Metrics**: Comprehensive visualization and analysis

## 📂 Folder Structure

```
QuantResearch/
├── config/              (Configuration & API keys)
├── database/            (Master CSV data files)
├── db/                  (Database helpers & scripts)
├── notebooks/           (Jupyter analysis notebooks)
└── output/              (Generated outputs)
```

## 🔧 Setup & Installation

### 1. Database Setup
```bash
# Initialize database & tables
python3 db/db_init.py
```

### 2. Market Data Collection
```bash
# Start fetching marketcap data (runs every 15 min during market hours)
python3 db/market_data_fetcher.py
```

### 3. Visualization
```bash
# Open Jupyter notebook for market analysis
jupyter notebook notebooks/01_market_data_visualization.ipynb
```

## 📊 Data Pipeline

```
yfinance API
     ↓
market_data_fetcher.py (runs 15 min intervals)
     ↓
MySQL: market_data table
     ↓
Jupyter Notebooks (visualization & analysis)
```

## 🕐 Market Hours (IDX)

- **Sesi I**: 08:45 - 12:00 (Kamis), 08:45 - 11:30 (Jumat)
- **Sesi II**: 13:30 - 16:15 (Kamis), 14:00 - 16:15 (Jumat)

Market data updates every 15 minutes during these hours.

## 📝 Notebooks

### 01_market_data_visualization.ipynb
Visualize market data with:
- Latest marketcap table
- Top 50 stocks by marketcap
- Sector distribution analysis
- Data quality metrics
- Historical trends

---

**Last Updated**: February 7, 2026
