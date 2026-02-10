"""
Database Helper Module
Provides easy access to database queries for the 4-layer system
"""

import mysql.connector
from mysql.connector import errorcode
import pandas as pd
from contextlib import contextmanager
import os
import sys

# Add parent directory to path for config imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DB_CONFIG


class DatabaseManager:
    """Manages database connections and queries"""
    
    def __init__(self):
        self.config = DB_CONFIG
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = mysql.connector.connect(**self.config)
        try:
            yield conn
        finally:
            conn.close()
    
    # ========== SAHAM QUERIES ==========
    
    def get_all_saham(self):
        """Get all stocks"""
        with self.get_connection() as conn:
            query = "SELECT kode_saham, nama_saham, sektor, subsector FROM saham ORDER BY sektor"
            df = pd.read_sql(query, conn)
            return df
    
    def get_saham_by_sektor(self, sektor):
        """Get stocks by sector"""
        with self.get_connection() as conn:
            query = f"SELECT kode_saham, nama_saham FROM saham WHERE sektor = %s"
            df = pd.read_sql(query, conn, params=(sektor,))
            return df
    
    def get_saham_info(self, kode_saham):
        """Get detailed info for a specific stock"""
        with self.get_connection() as conn:
            query = """
            SELECT kode_saham, nama_saham, sektor, subsector, listing_date 
            FROM saham 
            WHERE kode_saham = %s
            """
            df = pd.read_sql(query, conn, params=(kode_saham,))
            return df.to_dict('records')[0] if not df.empty else None
    
    def search_saham(self, keyword):
        """Search stocks by name or code"""
        with self.get_connection() as conn:
            query = """
            SELECT kode_saham, nama_saham, sektor 
            FROM saham 
            WHERE kode_saham LIKE %s OR nama_saham LIKE %s
            LIMIT 50
            """
            df = pd.read_sql(query, conn, params=(f"%{keyword}%", f"%{keyword}%"))
            return df
    
    # ========== BROKER QUERIES ==========
    
    def get_all_brokers(self):
        """Get all brokers"""
        with self.get_connection() as conn:
            query = "SELECT kode_broker, nama_broker FROM broker ORDER BY nama_broker"
            df = pd.read_sql(query, conn)
            return df
    
    def get_broker_info(self, kode_broker):
        """Get detailed info for a specific broker"""
        with self.get_connection() as conn:
            query = """
            SELECT kode_broker, nama_broker, deskripsi 
            FROM broker 
            WHERE kode_broker = %s
            """
            df = pd.read_sql(query, conn, params=(kode_broker,))
            return df.to_dict('records')[0] if not df.empty else None
    
    # ========== INSTITUTIONAL FLOW QUERIES ==========
    
    def add_institutional_flow(self, data):
        """
        Add institutional flow record
        data = {
            'kode_saham': str,
            'kode_broker': str,
            'tanggal': date,
            'volume_buy': int,
            'volume_sell': int,
            'net_volume': int,
            'value_buy': float,
            'value_sell': float,
            'net_value': float
        }
        """
        with self.get_connection() as conn:
            query = """
            INSERT INTO institutional_flow 
            (kode_saham, kode_broker, tanggal, volume_buy, volume_sell, net_volume, value_buy, value_sell, net_value)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor = conn.cursor()
            cursor.execute(query, (
                data['kode_saham'],
                data.get('kode_broker'),
                data['tanggal'],
                data.get('volume_buy'),
                data.get('volume_sell'),
                data.get('net_volume'),
                data.get('value_buy'),
                data.get('value_sell'),
                data.get('net_value')
            ))
            conn.commit()
            cursor.close()
            return cursor.lastrowid
    
    def get_whale_accumulation(self, kode_saham, days=30):
        """Get institutional accumulation for a stock (last N days)"""
        with self.get_connection() as conn:
            query = f"""
            SELECT tanggal, kode_broker, nama_broker, net_volume, net_value
            FROM institutional_flow
            JOIN broker ON institutional_flow.kode_broker = broker.kode_broker
            WHERE kode_saham = %s AND tanggal >= DATE_SUB(CURDATE(), INTERVAL {days} DAY)
            ORDER BY tanggal DESC, net_volume DESC
            """
            df = pd.read_sql(query, conn, params=(kode_saham,))
            return df
    
    def get_broker_top_accumulations(self, kode_broker, top_n=20):
        """Get top accumulated stocks by a specific broker"""
        with self.get_connection() as conn:
            query = f"""
            SELECT saham.kode_saham, saham.nama_saham, saham.sektor,
                   SUM(institutional_flow.net_volume) as total_net_volume,
                   SUM(institutional_flow.net_value) as total_net_value
            FROM institutional_flow
            JOIN saham ON institutional_flow.kode_saham = saham.kode_saham
            WHERE kode_broker = %s
            GROUP BY institutional_flow.kode_saham
            ORDER BY total_net_volume DESC
            LIMIT {top_n}
            """
            df = pd.read_sql(query, conn, params=(kode_broker,))
            return df
    
    def get_sektor_top_brokers(self, sektor, top_n=10):
        """Get brokers with most activity in a sector"""
        with self.get_connection() as conn:
            query = f"""
            SELECT institutional_flow.kode_broker, broker.nama_broker,
                   COUNT(DISTINCT institutional_flow.kode_saham) as stock_count,
                   SUM(institutional_flow.net_volume) as total_net_volume
            FROM institutional_flow
            JOIN saham ON institutional_flow.kode_saham = saham.kode_saham
            JOIN broker ON institutional_flow.kode_broker = broker.kode_broker
            WHERE saham.sektor = %s
            GROUP BY institutional_flow.kode_broker
            ORDER BY total_net_volume DESC
            LIMIT {top_n}
            """
            df = pd.read_sql(query, conn, params=(sektor,))
            return df
    
    def get_sector_summary(self):
        """Get summary of all sectors"""
        with self.get_connection() as conn:
            query = """
            SELECT sektor, COUNT(*) as stock_count, COUNT(DISTINCT subsector) as subsector_count
            FROM saham
            GROUP BY sektor
            ORDER BY stock_count DESC
            """
            df = pd.read_sql(query, conn)
            return df
    
    def get_db_stats(self):
        """Get database statistics"""
        stats = {}
        
        with self.get_connection() as conn:
            # Count stocks
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM saham")
            stats['total_stocks'] = cursor.fetchone()[0]
            
            # Count brokers
            cursor.execute("SELECT COUNT(*) as count FROM broker")
            stats['total_brokers'] = cursor.fetchone()[0]
            
            # Count flows
            cursor.execute("SELECT COUNT(*) as count FROM institutional_flow")
            stats['total_flows'] = cursor.fetchone()[0]
            
            # Count sectors
            cursor.execute("SELECT COUNT(DISTINCT sektor) as count FROM saham")
            stats['total_sectors'] = cursor.fetchone()[0]
            
            cursor.close()
        
        return stats
    
    # ========== MARKET DATA QUERIES ==========
    
    def get_latest_market_data(self, limit=100):
        """Get latest market data"""
        with self.get_connection() as conn:
            query = """
            SELECT kode_saham, marketcap_idr, price, volume, tanggal, waktu
            FROM market_data
            ORDER BY tanggal DESC, waktu DESC
            LIMIT %s
            """
            df = pd.read_sql(query, conn, params=(limit,))
            return df
    
    def get_market_data_by_date(self, tanggal):
        """Get market data for specific date"""
        with self.get_connection() as conn:
            query = """
            SELECT kode_saham, marketcap_idr, price, volume, tanggal, waktu
            FROM market_data
            WHERE tanggal = %s
            ORDER BY marketcap_idr DESC
            """
            df = pd.read_sql(query, conn, params=(tanggal,))
            return df
    
    def get_market_data_by_saham(self, kode_saham, limit=30):
        """Get historical market data for specific stock"""
        with self.get_connection() as conn:
            query = """
            SELECT kode_saham, marketcap_idr, price, volume, tanggal, waktu
            FROM market_data
            WHERE kode_saham = %s
            ORDER BY tanggal DESC, waktu DESC
            LIMIT %s
            """
            df = pd.read_sql(query, conn, params=(kode_saham, limit))
            return df
    
    def get_top_marketcap(self, tanggal, limit=50):
        """Get top N stocks by marketcap for specific date"""
        with self.get_connection() as conn:
            query = """
            SELECT s.kode_saham, s.nama_saham, s.sektor, 
                   m.marketcap_idr, m.price, m.volume, m.tanggal, m.waktu
            FROM market_data m
            JOIN saham s ON m.kode_saham = s.kode_saham
            WHERE m.tanggal = %s
            ORDER BY m.marketcap_idr DESC
            LIMIT %s
            """
            df = pd.read_sql(query, conn, params=(tanggal, limit))
            return df


# Singleton instance
db = DatabaseManager()
