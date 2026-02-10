"""
API Configuration - Datasaham & YFinance
Centralized API configuration and helper functions
"""

# ============================================
# DATASAHAM API CONFIGURATION
# ============================================

DATASAHAM = {
    "base_url": "https://api.datasaham.io/api",
    "api_key": "sbk_b0df044971dab991ddb075caf87b8df83ad0fbd2d67d3a92",
    "version": "v1.0.0",
    "headers": {
        "x-api-key": "sbk_b0df044971dab991ddb075caf87b8df83ad0fbd2d67d3a92",
        "Content-Type": "application/json"
    },
    "rate_limits": {
        "free": {
            "requests_per_minute": 60,
            "requests_per_day": 1000,
        },
        "premium": {
            "requests_per_minute": 300,
            "requests_per_day": 50000,
        }
    },
    "documentation": "https://api.datasaham.io/swagger"
}

# ============================================
# YFINANCE CONFIGURATION
# ============================================

YFINANCE = {
    "base_url": "https://query1.finance.yahoo.com",
    "free_tier": True,
    "supports": ["stocks", "crypto", "forex", "commodities"],
    "main_uses": [
        "OHLCV data (US, Global stocks)",
        "Historical price data",
        "Volume data",
        "Dividend information"
    ]
}

# ============================================
# ENDPOINT MAPPINGS
# ============================================

API_ENDPOINTS = {
    # ==== CORE ENDPOINTS FOR TRADING STRATEGY ====
    
    "sector_rotation": {
        "api": "datasaham",
        "endpoint": "/analysis/retail/sector-rotation",
        "method": "GET",
        "tier": "premium",
        "use_case": "Layer 1 - Identify hot/cold sectors",
        "description": "Get sector rotation analysis to identify bullish rotating sectors"
    },
    
    "broker_summary": {
        "api": "datasaham",
        "endpoint": "/market-detector/broker-summary/{symbol}",
        "method": "GET",
        "tier": "premium",
        "use_case": "Layer 2 - Get broker flows for stock",
        "description": "Get detailed broker activity and flow analysis for specific stock"
    },
    
    "whale_transactions": {
        "api": "datasaham",
        "endpoint": "/analysis/whale-transactions/{symbol}",
        "method": "GET",
        "tier": "premium",
        "use_case": "Layer 2 - Get whale accumulation",
        "description": "Detect large smart money accumulation patterns"
    },
    
    "bandar_accumulation": {
        "api": "datasaham",
        "endpoint": "/analysis/bandar/accumulation/{symbol}",
        "method": "GET",
        "tier": "premium",
        "use_case": "Layer 3 - Verify institutional activity",
        "description": "Get bandar/market maker accumulation analysis"
    },
    
    "ohlcv_data": {
        "api": "datasaham",
        "endpoint": "/chart/{symbol}/{timeframe}",
        "method": "GET",
        "tier": "free",
        "use_case": "Layer 3 - Get price data for bid/offer verification",
        "description": "Get OHLCV chart data for technical analysis"
    },
    
    "orderbook": {
        "api": "datasaham",
        "endpoint": "/emiten/{symbol}/orderbook",
        "method": "GET",
        "tier": "premium",
        "use_case": "Layer 3 - Get bid/ask spread",
        "description": "Real-time order book with bid/ask levels"
    },
    
    "technical_analysis": {
        "api": "datasaham",
        "endpoint": "/analysis/technical/{symbol}",
        "method": "GET",
        "tier": "premium",
        "use_case": "Layer 3 - Verify technical patterns",
        "description": "Get technical indicators and analysis"
    },
    
    # ==== SUPPORT ENDPOINTS ====
    
    "search": {
        "api": "datasaham",
        "endpoint": "/main/search",
        "method": "GET",
        "tier": "free",
        "use_case": "Search stocks by name/code",
        "description": "Search for stocks by symbol or name"
    },
    
    "trending": {
        "api": "datasaham",
        "endpoint": "/main/trending",
        "method": "GET",
        "tier": "free",
        "use_case": "Get trending stocks",
        "description": "Get current trending stocks"
    },
    
    "broker_codes": {
        "api": "datasaham",
        "endpoint": "/main/broker-codes",
        "method": "GET",
        "tier": "free",
        "use_case": "Get all broker codes reference",
        "description": "Get list of all broker codes"
    },
    
    "sectors": {
        "api": "datasaham",
        "endpoint": "/sectors/",
        "method": "GET",
        "tier": "free",
        "use_case": "Get all sectors",
        "description": "Get list of all market sectors"
    },
    
    "company_info": {
        "api": "datasaham",
        "endpoint": "/emiten/{symbol}/info",
        "method": "GET",
        "tier": "free",
        "use_case": "Get company information",
        "description": "Get basic company information"
    },
}

# ============================================
# TIMEFRAME CONSTANTS
# ============================================

TIMEFRAMES = {
    "1m": "1 minute",
    "5m": "5 minutes",
    "15m": "15 minutes",
    "30m": "30 minutes",
    "1h": "1 hour",
    "4h": "4 hours",
    "1d": "1 day",
    "1w": "1 week",
    "1mo": "1 month"
}

# ============================================
# MOVERS TYPES
# ============================================

MOVER_TYPES = {
    "gainer": "Top gainers",
    "loser": "Top losers",
    "value": "Top value traded",
    "volume": "Top volume",
    "net_foreign_buy": "Net foreign buy",
    "net_foreign_sell": "Net foreign sell"
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_datasaham_headers():
    """Get Datasaham API headers"""
    return DATASAHAM["headers"]


def get_datasaham_url(endpoint_path):
    """Build full Datasaham API URL"""
    return f"{DATASAHAM['base_url']}{endpoint_path}"


def get_endpoint_config(endpoint_name):
    """Get full configuration for an endpoint"""
    if endpoint_name in API_ENDPOINTS:
        return API_ENDPOINTS[endpoint_name]
    return None


def is_premium_tier(endpoint_name):
    """Check if endpoint requires premium tier"""
    endpoint = get_endpoint_config(endpoint_name)
    return endpoint and endpoint.get("tier") == "premium"


def get_endpoints_by_tier(tier):
    """Get all endpoints for a specific tier"""
    return {
        name: config for name, config in API_ENDPOINTS.items()
        if config.get("tier") == tier
    }


def get_endpoints_by_layer(layer_num):
    """Get all endpoints used for a specific layer"""
    layer_map = {
        1: ["sector_rotation"],
        2: ["broker_summary", "whale_transactions"],
        3: ["bandar_accumulation", "ohlcv_data", "orderbook", "technical_analysis"],
        4: ["technical_analysis", "ohlcv_data"]
    }
    
    layer_endpoints = layer_map.get(layer_num, [])
    return {
        name: API_ENDPOINTS[name] for name in layer_endpoints
        if name in API_ENDPOINTS
    }
