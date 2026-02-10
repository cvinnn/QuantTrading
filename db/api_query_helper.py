"""
API Query Helper - Query endpoints from database
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database_helper import db
import pandas as pd


def get_api_endpoint(endpoint_name):
    """Get specific endpoint from database"""
    with db.get_connection() as conn:
        query = "SELECT * FROM api_endpoints WHERE endpoint_name = %s"
        df = pd.read_sql(query, conn, params=(endpoint_name,))
        return df.to_dict('records')[0] if not df.empty else None


def get_endpoints_by_category(category):
    """Get all endpoints in a category"""
    with db.get_connection() as conn:
        query = "SELECT * FROM api_endpoints WHERE category = %s ORDER BY endpoint_name"
        df = pd.read_sql(query, conn, params=(category,))
        return df


def get_all_categories():
    """Get all endpoint categories"""
    with db.get_connection() as conn:
        query = "SELECT DISTINCT category FROM api_endpoints ORDER BY category"
        df = pd.read_sql(query, conn)
        return df['category'].tolist()


def get_endpoints_by_tier(tier):
    """Get all endpoints by rate limit tier"""
    with db.get_connection() as conn:
        query = "SELECT * FROM api_endpoints WHERE rate_limit_tier = %s ORDER BY category, endpoint_name"
        df = pd.read_sql(query, conn, params=(tier,))
        return df


def get_endpoints_by_use_case(use_case_keyword):
    """Search endpoints by use case"""
    with db.get_connection() as conn:
        query = "SELECT * FROM api_endpoints WHERE use_case LIKE %s ORDER BY category"
        df = pd.read_sql(query, conn, params=(f"%{use_case_keyword}%",))
        return df


def get_layer_endpoints(layer_num):
    """Get endpoints used for specific layer"""
    layer_keywords = {
        1: "Layer 1",
        2: "Layer 2",
        3: "Layer 3",
        4: "Layer 4"
    }
    
    keyword = layer_keywords.get(layer_num)
    if keyword:
        return get_endpoints_by_use_case(keyword)
    return pd.DataFrame()


def get_core_endpoints():
    """Get core endpoints used for trading strategy"""
    core_uses = [
        "Layer 1",
        "Layer 2",
        "Layer 3",
        "Layer 4"
    ]
    
    with db.get_connection() as conn:
        placeholders = ", ".join(["%s"] * len(core_uses))
        query = f"""
        SELECT * FROM api_endpoints 
        WHERE use_case LIKE ANY (SELECT '%' || %s || '%')
        ORDER BY category
        """
        # Use simple approach instead
        all_endpoints = []
        for use_case in core_uses:
            query = "SELECT * FROM api_endpoints WHERE use_case LIKE %s"
            df = pd.read_sql(query, conn, params=(f"%{use_case}%",))
            all_endpoints.append(df)
        
        if all_endpoints:
            return pd.concat(all_endpoints, ignore_index=True).drop_duplicates(subset=['id'])
        return pd.DataFrame()


def list_all_endpoints():
    """List all endpoints with summary"""
    with db.get_connection() as conn:
        query = "SELECT category, COUNT(*) as count FROM api_endpoints GROUP BY category ORDER BY category"
        df = pd.read_sql(query, conn)
        return df


def print_api_summary():
    """Print API endpoints summary"""
    print("\n" + "="*80)
    print("📡 DATASAHAM API ENDPOINTS REGISTRY")
    print("="*80 + "\n")
    
    # Summary by category
    print("📊 Endpoints by Category:")
    print("-"*80)
    summary = list_all_endpoints()
    print(summary.to_string(index=False))
    
    # Summary by tier
    print("\n\n💾 Endpoints by Tier:")
    print("-"*80)
    with db.get_connection() as conn:
        query = "SELECT rate_limit_tier, COUNT(*) as count FROM api_endpoints GROUP BY rate_limit_tier ORDER BY rate_limit_tier"
        df = pd.read_sql(query, conn)
        print(df.to_string(index=False))
    
    # Core endpoints
    print("\n\n🎯 CORE ENDPOINTS FOR TRADING STRATEGY:")
    print("-"*80)
    for layer in [1, 2, 3, 4]:
        endpoints = get_layer_endpoints(layer)
        if not endpoints.empty:
            print(f"\n**LAYER {layer}**: {len(endpoints)} endpoints")
            for idx, row in endpoints.iterrows():
                print(f"  • {row['endpoint_name']}")
                print(f"    → {row['url_path']}")
                print(f"    → {row['description']}")
                print()
    
    print("="*80 + "\n")


if __name__ == "__main__":
    print_api_summary()
