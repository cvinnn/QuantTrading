"""
Configuration file - 3 Essential Components
"""

# 1. API KEY
DATASAHAM_API_KEY = "sbk_b0df044971dab991ddb075caf87b8df83ad0fbd2d67d3a92"
DATASAHAM_BASE_URL = "https://api.datasaham.io/api"

# 2. SAHAM LIST PATH
SAHAM_LIST_FILE = "saham_list.csv"

# 3. MOMENTUM INDICATOR PATH
MOMENTUM_INDICATOR_FILE = "idx_momentum_indicator.py"

# Default settings
OUTPUT_FOLDER = "output"
DATA_FOLDER = "data"

# ==== DATABASE CONFIGURATION (XAMPP MySQL) ====
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Change if you set a password in XAMPP
    "database": "quantresearch_db",
    "port": 3306,
}

# Master CSV files location
CSV_FILES = {
    "saham_master": "database/Daftar Saham  - 20260206.csv",
    "broker_summary": "database/Ringkasan Broker-20260205.csv",
}
