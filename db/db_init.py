"""
Database Initialization & Migration Script
Migrates CSV files from database/ folder to MySQL (XAMPP)
"""

import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import os
import sys

# Add parent directory to path for config imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DB_CONFIG, CSV_FILES


def create_database():
    """Create database if it doesn't exist"""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            port=DB_CONFIG["port"],
        )
        cursor = conn.cursor()
        
        # Create database
        try:
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
            print(f"✅ Database '{DB_CONFIG['database']}' created successfully")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DB_CREATE_EXISTS:
                print(f"ℹ️ Database '{DB_CONFIG['database']}' already exists")
            else:
                raise
        
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        return False


def create_tables():
    """Create tables for saham and broker data"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Table for Saham (stocks)
        create_saham_table = """
        CREATE TABLE IF NOT EXISTS saham (
            id INT AUTO_INCREMENT PRIMARY KEY,
            kode_saham VARCHAR(10) UNIQUE NOT NULL,
            nama_saham VARCHAR(255),
            sektor VARCHAR(100),
            subsector VARCHAR(100),
            listing_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_kode (kode_saham),
            INDEX idx_sektor (sektor)
        );
        """
        
        # Table for Broker
        create_broker_table = """
        CREATE TABLE IF NOT EXISTS broker (
            id INT AUTO_INCREMENT PRIMARY KEY,
            kode_broker VARCHAR(10) UNIQUE NOT NULL,
            nama_broker VARCHAR(255),
            deskripsi TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_kode (kode_broker)
        );
        """
        
        # Table for Institutional Flow (untuk tracking whale/broker accumulation)
        create_flow_table = """
        CREATE TABLE IF NOT EXISTS institutional_flow (
            id INT AUTO_INCREMENT PRIMARY KEY,
            kode_saham VARCHAR(10) NOT NULL,
            kode_broker VARCHAR(10),
            tanggal DATE NOT NULL,
            volume_buy BIGINT,
            volume_sell BIGINT,
            net_volume BIGINT,
            value_buy DECIMAL(18, 2),
            value_sell DECIMAL(18, 2),
            net_value DECIMAL(18, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (kode_saham) REFERENCES saham(kode_saham),
            FOREIGN KEY (kode_broker) REFERENCES broker(kode_broker),
            INDEX idx_saham_date (kode_saham, tanggal),
            INDEX idx_broker_date (kode_broker, tanggal)
        );
        """
        
        # Table for Market Data (marketcap, price from yfinance)
        create_market_data_table = """
        CREATE TABLE IF NOT EXISTS market_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            kode_saham VARCHAR(10) NOT NULL,
            marketcap_idr BIGINT,
            price DECIMAL(15, 2),
            volume BIGINT,
            tanggal DATE NOT NULL,
            waktu TIME NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (kode_saham) REFERENCES saham(kode_saham),
            INDEX idx_saham_date (kode_saham, tanggal),
            UNIQUE KEY unique_saham_datetime (kode_saham, tanggal, waktu)
        );
        """
        
        for table_sql in [create_saham_table, create_broker_table, create_flow_table, create_market_data_table]:
            cursor.execute(table_sql)
        
        print("✅ All tables created successfully")
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"❌ Error creating tables: {err}")
        return False


def import_saham_data():
    """Import saham master list from CSV"""
    try:
        # Check if CSV file exists
        if not os.path.exists(CSV_FILES["saham_master"]):
            print(f"❌ File not found: {CSV_FILES['saham_master']}")
            return False
        
        # Read CSV
        df = pd.read_csv(CSV_FILES["saham_master"])
        print(f"📄 Loaded {len(df)} stocks from CSV")
        
        # Connect to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Insert data
        insert_query = """
        INSERT INTO saham (kode_saham, nama_saham, sektor, subsector)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        nama_saham = VALUES(nama_saham),
        sektor = VALUES(sektor),
        subsector = VALUES(subsector),
        updated_at = CURRENT_TIMESTAMP
        """
        
        count = 0
        for idx, row in df.iterrows():
            try:
                cursor.execute(insert_query, (
                    row.get('Kode', ''),
                    row.get('Nama Perusahaan', ''),
                    row.get('Papan Pencatatan', ''),  # Papan (Main/Development)
                    ''  # subsector (not available in CSV)
                ))
                count += 1
            except Exception as e:
                print(f"⚠️ Error inserting row {idx}: {e}")
                continue
        
        conn.commit()
        print(f"✅ Imported {count} stocks to database")
        cursor.close()
        conn.close()
        return True
    except Exception as err:
        print(f"❌ Error importing saham data: {err}")
        return False


def import_broker_data():
    """Import broker summary from CSV"""
    try:
        # Check if CSV file exists
        if not os.path.exists(CSV_FILES["broker_summary"]):
            print(f"❌ File not found: {CSV_FILES['broker_summary']}")
            return False
        
        # Read CSV
        df = pd.read_csv(CSV_FILES["broker_summary"])
        print(f"📄 Loaded {len(df)} brokers from CSV")
        
        # Connect to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Insert data
        insert_query = """
        INSERT INTO broker (kode_broker, nama_broker, deskripsi)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        nama_broker = VALUES(nama_broker),
        deskripsi = VALUES(deskripsi),
        updated_at = CURRENT_TIMESTAMP
        """
        
        count = 0
        for idx, row in df.iterrows():
            try:
                cursor.execute(insert_query, (
                    row.get('Kode Perusahaan', ''),
                    row.get('Nama Perusahaan', ''),
                    f"Volume: {row.get('Volume', '')}, Nilai: {row.get('Nilai', '')}, Frekuensi: {row.get('Frekuensi', '')}"
                ))
                count += 1
            except Exception as e:
                print(f"⚠️ Error inserting row {idx}: {e}")
                continue
        
        conn.commit()
        print(f"✅ Imported {count} brokers to database")
        cursor.close()
        conn.close()
        return True
    except Exception as err:
        print(f"❌ Error importing broker data: {err}")
        return False


def main():
    """Run all database initialization steps"""
    print("\n" + "="*50)
    print("🗄️  Database Initialization (XAMPP MySQL)")
    print("="*50 + "\n")
    
    print("Step 1: Creating database...")
    if not create_database():
        return False
    
    print("\nStep 2: Creating tables...")
    if not create_tables():
        return False
    
    print("\nStep 3: Importing saham master list...")
    if not import_saham_data():
        return False
    
    print("\nStep 4: Importing broker summary...")
    if not import_broker_data():
        return False
    
    print("\n" + "="*50)
    print("✅ Database initialization completed!")
    print("="*50 + "\n")
    return True


if __name__ == "__main__":
    main()
