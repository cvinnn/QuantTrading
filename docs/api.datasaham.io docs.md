

06/02/26, 23.13Datasaham.io API
Page 1 of 56https://api.datasaham.io/swagger#description/-global-market
v1.0.0OAS 3.0.3
## Datasaham.io
## API
## Tentang
Datasaham.io API adalah layanan RESTful API
komprehensif untuk analisis pasar saham
Indonesia (IDX). Dibangun dengan prinsip clean
architecture, API ini menyediakan data pasar
real-time, analitik canggih, dan insight trading
yang cerdas.
Global Market Data API
Butuh data pasar global? Kunjungi OHLC.dev -
API kami untuk data pasar global:
Stocks: US, EU, Asia markets (NYSE,
NASDAQ, LSE, TSE, dll)
Crypto: Bitcoin, Ethereum, dan 1000+
altcoins
Forex: Major, minor, dan exotic pairs
## Commodities: Gold, Silver, Oil, Natural Gas,
dll
Indices: S&P 500, NASDAQ, Dow Jones,
FTSE, Nikkei, dll
https://ohlc.dev - Real-time & historical
OHLCV data untuk global markets
## Fitur Utama
## Calendar
Download OpenAPI Document
Download OpenAPI Document
## Search
⌘ KOpen Search
## KEYBOARD SHORTCUT:COMMAND
Get Sector Correlation with
## Global Factors
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
## Movers
## Close Group
## Get Market Mover Data
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
## Market Detector
## Close Group
Get broker activity detail
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
Get top brokers
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
Get top stocks
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
Get broker summary for a
stock
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
## Bandarmology
## Close Group
## Bandar Accumulation
## Detector
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
## Bandar Distribution Detector
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
## Smart Money Flow Tracker
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
## Pump & Dump Detector
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
## Retail Opportunity
## Close Group
## Multibagger Candidate
## Scanner
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
## Breakout Alert System
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
Risk-Reward Calculator
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
## Sector Rotation Analyzer
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
## Market Sentiment
## Close Group
Retail vs Bandar Sentiment
## Analysis
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
IPO Momentum Tracker
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
## Advanced Analytics
## Close Group
## Correlation Matrix Calculator
## GETGETGETGET
## HTTP METHOD: HTTP METHOD: HTTP METHOD: HTTP METHOD:
## Whale Transaction Detector
## GETGETGETGET

06/02/26, 23.13Datasaham.io API
Page 2 of 56https://api.datasaham.io/swagger#description/-global-market
## Calendar
Kalender aksi korporasi - dividen, stock split,
IPO, RUPS, dan corporate actions lainnya
## Main
Endpoint umum - pencarian saham, trending
stocks, dan informasi pasar
## Global Market
Data pasar global - indeks dunia, komoditas,
forex, dan analisis dampaknya terhadap IDX
## Chart
Data OHLCV dan chart - daily, weekly, monthly,
dan intraday (15m, 30m, 1h, 2h, 3h, 4h)
## Sectors
Data sektor dan subsektor - performa sektor,
daftar perusahaan per sektor
## Movers
Market movers - top gainer, top loser, top
value, top volume, net foreign buy/sell
## Market Detector
Analisis aktivitas broker - broker activity, top
broker, top stock, broker summary
## Bandarmology
Analisis bandar/market maker - deteksi
akumulasi, distribusi, smart money flow, pump
& dump
## Retail Opportunity
Open API Client
Powered by Scalar

06/02/26, 23.13Datasaham.io API
Page 3 of 56https://api.datasaham.io/swagger#description/-global-market
## Retail Opportunity
Peluang untuk retail investor - multibagger
scanner, breakout alerts, risk-reward calculator,
sector rotation
## Market Sentiment
Analisis sentimen pasar - retail vs bandar
sentiment, IPO momentum tracker
## Advanced Analytics
Analitik lanjutan - correlation matrix, whale
transaction detector, insider screening,
technical analyst, global screener
## Emiten
Informasi emiten - profil perusahaan, data
keuangan, broker summary, insider trading,
tradebook chart
## BETA
Fitur eksperimental - insights, earnings,
equities, key ratios (data dari Datasaham.io)
## Autentikasi
Semua endpoint API memerlukan autentikasi
menggunakan API key. Sertakan API key Anda
di request header:
x-api-key: your_api_key_here
## Rate Limiting
Request API dibatasi berdasarkan tier
langganan Anda. Cek response headers untuk
penggunaan saat ini:

06/02/26, 23.13Datasaham.io API
Page 4 of 56https://api.datasaham.io/swagger#description/-global-market
API health check
## Health
## Operations
## GET/
GET/health
## Show More
penggunaan saat ini:
X-RateLimit-Limit - Maksimum request yang
diizinkan
X-RateLimit-Remaining - Sisa request dalam
window saat ini
X-RateLimit-Reset - Waktu reset rate limit
## Server
https://api.datasaham.io
## Client Libraries
## Shell Curl
## Authentication
## Required
ApiKeyAuth
Enter your API Key
## Name:
x-api-key
## Value:••••••••••••••••••••••••••••••••••••••••••••••••••••
ShellRubyNode.jsPHPPython

06/02/26, 23.13Datasaham.io API
Page 5 of 56https://api.datasaham.io/swagger#description/-global-market
Corporate action calendar events
## Calendar
## Operations
GET/api/calendar/dividend
GET/api/calendar/bonus
GET/api/calendar/stock-split
GET/api/calendar/right-issue
GET/api/calendar/warrant
GET/api/calendar/rups
GET/api/calendar/ipo
GET/api/calendar/economic
GET/api/calendar/tender-offer
GET/api/calendar/today
## Show More
General endpoints
## Main
## Operations
GET/api/main/search
GET/api/main/trending
GET/api/main/morning-briefing
GET/api/main/commodities-impact
GET/api/main/forex-idr-impact
GET/api/main/us-stocks-parent
GET/api/main/broker-codes
## Show More

06/02/26, 23.13Datasaham.io API
Page 6 of 56https://api.datasaham.io/swagger#description/-global-market
## Show More
Global market data (indices, commodities,
forex) and impact analysis on IDX
## Global
## Market
## Operations
GET/api/global/market-overview
GET/api/global/indices-impact
GET/api/global/impact-analysis
## Show More
Chart and OHLCV data
## Chart
## Operations
GET/api/chart/{symbol}/{timeframe}
Get Open, High, Low, Close, Volume (OHLCV)
chart data for a stock symbol with specified
timeframe
Get OHLCV
## Chart Data

06/02/26, 23.13Datasaham.io API
Page 7 of 56https://api.datasaham.io/swagger#description/-global-market
## Path Parameters
## Query Parameters
string·min length:  1required
Stock symbol
symbolExamples
string·enumrequired
Chart timeframe (use daily with different date ranges
for weekly/monthly data)
timeframeExamples
daily
## 15m
## 30m
## 1h
## 2h
## 3h
## 4h
string
## ·^\d{4}-\d{2}-\d{2}$
required
Start date (YYYY-MM-DD) - newer date, auto-
converted to unix timestamp for intraday intervals
from
## Example
string
## ·^\d{4}-\d{2}-\d{2}$
required
End date (YYYY-MM-DD) - older date, auto-converted
to unix timestamp for intraday intervals
to
## Example
Any ofstring
limit
string·numeric·default: 0
Limit number of results (0 = no limit)
GET/api/chart/{symbol}/
## {time
## ...
## Shell Curl
1curl 'https:"#api.datasaham.io/api/chart/BBCA/daily?from=2026-01-05&to=2024-11-11' \
## 2  "$header 'x-api-key: ·····'
## Test Request

06/02/26, 23.13Datasaham.io API
Page 8 of 56https://api.datasaham.io/swagger#description/-global-market
## Test Request
Sector, subsector, and company data
## Sectors
## Operations
GET/api/sectors/
GET/api/sectors/{sectorId}/subsectors
GET/api/sectors/{sectorId}/subsectors/{subSectorId}/companies
GET/api/sectors/correlation/{sector}
Get list of all available sectors
## Get All
## Sectors
GET/api/sectors/Shell Curl
1curl https:"#api.datasaham.io/api/sectors/ \
## 2  "$header 'x-api-key: ·····'
## Test Request

06/02/26, 23.13Datasaham.io API
Page 9 of 56https://api.datasaham.io/swagger#description/-global-market
Get list of subsectors for a specific sector
## Path Parameters
## Get
SubSectors
string·min length:  1required
Sector ID
sectorIdExamples
GET/api/sectors/{sectorId}
## /s
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/sectors/7/subsectors \
## 2  "$header 'x-api-key: ·····'
## Test Request

06/02/26, 23.13Datasaham.io API
Page 10 of 56https://api.datasaham.io/swagger#description/-global-market
Get list of companies in a specific sector and
subsector with detailed information including
price, volume, market cap, etc.
## Path Parameters
## Get
## Companies
by Sector &
SubSector
string·min length:  1required
Sector ID
sectorIdExamples
string·min length:  1required
SubSector ID
subSectorId
## Examples
GET/api/sectors/{sectorId}
## /s
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/sectors/7/subsectors/19/companies \
## 2  "$header 'x-api-key: ·····'
## Test Request

06/02/26, 23.13Datasaham.io API
Page 11 of 56https://api.datasaham.io/swagger#description/-global-market
Analyze how global commodities, currencies,
and indices affect IDX sectors. Shows current
impact and outlook based on real-time global
market data.
## Path Parameters
## Get Sector
## Correlation
with Global
## Factors
stringrequired
Sector name (energy, mining, plantation, banking,
consumer, property, technology, transportation)
sectorExamples
GET/api/sectors/correlation/
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/sectors/correlation/energy \
## 2  "$header 'x-api-key: ·····'
## Test Request

06/02/26, 23.13Datasaham.io API
Page 12 of 56https://api.datasaham.io/swagger#description/-global-market
Market movers (top gainer, top loser, etc.)
## Movers
## Operations
GET/api/movers/{moverType}
Get market mover data including top gainers,
top losers, top value, top volume, and IEP-IEV
data.
## Regular Mover Types:
## Get Market
## Mover Data

06/02/26, 23.13Datasaham.io API
Page 13 of 56https://api.datasaham.io/swagger#description/-global-market
top-gainer - Stocks with highest
percentage gain
top-loser - Stocks with highest percentage
loss
top-value - Stocks with highest trading
value
top-volume - Stocks with highest trading
volume
top-frequency - Stocks with highest trading
frequency
net-foreign-buy - Stocks with highest net
foreign buy
net-foreign-sell - Stocks with highest net
foreign sell
IEP-IEV Mover Types (Special Monitoring
## Board):
iep-current-top-gainer - IEP current top
gainer
iep-current-top-loser - IEP current top loser
iep-prev-top-gainer - IEP previous top
gainer
iep-prev-top-loser - IEP previous top loser
iev-top-gainer - IEV top gainer
iev-top-loser - IEV top loser
ieval-top-gainer - IEVAL top gainer
ieval-top-loser - IEVAL top loser
## Filter Stocks:

06/02/26, 23.13Datasaham.io API
Page 14 of 56https://api.datasaham.io/swagger#description/-global-market
FILTER_STOCKS_TYPE_MAIN_BOARD - Main board
stocks
## FILTER_STOCKS_TYPE_DEVELOPMENT_BOARD -
Development board stocks
## FILTER_STOCKS_TYPE_ACCELERATION_BOARD -
Acceleration board stocks
FILTER_STOCKS_TYPE_NEW_ECONOMY_BOARD - New
economy board stocks
## FILTER_STOCKS_TYPE_SPECIAL_MONITORING_BOARD -
Special monitoring board (for IEP-IEV)
## Path Parameters
## Query Parameters
string·enumrequired
Market mover type
Show all values
moverTypeExamples
top-gainer
top-loser
top-value
top-volume
top-frequency
array string[]·enum
## ·default:
## ["FILTER_STOCKS_TYPE_MAIN_BOARD","FILT...
Stock board filters (can be multiple)
filterStocks
## FILTER_STOCKS_TYPE_MAIN_BOARD
## FILTER_STOCKS_TYPE_DEVELOPMENT_BOARD
## FILTER_STOCKS_TYPE_ACCELERATION_BOARD
## FILTER_STOCKS_TYPE_NEW_ECONOMY_BOARD
## FILTER_STOCKS_TYPE_SPECIAL_MONITORING_BOA
## RD
GET/api/movers/{moverType}Shell Curl
1curl https:"#api.datasaham.io/api/movers/top-gainer \
## 2  "$header 'x-api-key: ·····'

06/02/26, 23.13Datasaham.io API
Page 15 of 56https://api.datasaham.io/swagger#description/-global-market
## 2  "$header 'x-api-key: ·····'
## Test Request
Stock market analysis
## Market
## Detector
## Operations
GET/api/market-detector/broker-activity/{brokerCode}
GET/api/market-detector/top-broker
GET/api/market-detector/top-stock
GET/api/market-detector/broker-summary/{symbol}
Retrieve detailed broker activity information
including bandar detector and broker summary
## Path Parameters
## Query Parameters
Get broker
activity detail
stringrequired
Broker code (e.g., DH)
brokerCodeExamples

06/02/26, 23.13Datasaham.io API
Page 16 of 56https://api.datasaham.io/swagger#description/-global-market
Any ofstring
page
string·numeric·default: 0
Any ofstring
limit
string·numeric·default: 0
stringrequired
Start date (YYYY-MM-DD)
fromExample
stringrequired
End date (YYYY-MM-DD)
toExample
string·enum
·default: "TRANSACTION_TYPE_NET"required
Transaction type
transactionType
## TRANSACTION_TYPE_NET
## TRANSACTION_TYPE_GROSS
string·enum
·default: "MARKET_BOARD_ALL"required
Market board: ALL, REGULER (regular), NEGO
(negotiated), TUNAI (cash)
marketBoard
## MARKET_BOARD_ALL
## MARKET_BOARD_REGULER
## MARKET_BOARD_NEGO
## MARKET_BOARD_TUNAI
string·enum
·default: "INVESTOR_TYPE_ALL"required
Investor type
investorType
## INVESTOR_TYPE_ALL
## INVESTOR_TYPE_DOMESTIC
## INVESTOR_TYPE_FOREIGN
## GET
## /api/market-detector/brok
## ...
## Shell Curl

06/02/26, 23.13Datasaham.io API
Page 17 of 56https://api.datasaham.io/swagger#description/-global-market
## GET
## /api/market-detector/brok
## ...
## Shell Curl
1curl 'https:"#api.datasaham.io/api/market-detector/broker-activity/DH?from=2026-01-02&to=2026-01-02&transactionType=TRANSACTION_TYPE_NET&marketBoard=MARKET_BOARD_ALL&investorType=INVESTOR_TYPE_ALL' \
## 2  "$header 'x-api-key: ·····'
## Test Request
Retrieve list of top brokers sorted by various
criteria
## Query Parameters
Get top
brokers
string·enum
·default: "TB_SORT_BY_TOTAL_VALUE"required
Sort field
sort
## TB_SORT_BY_TOTAL_VALUE
## TB_SORT_BY_NET_VALUE
## TB_SORT_BY_TOTAL_VOLUME
string·enum·default: "ORDER_BY_DESC"
required
Sort order
order
## ORDER_BY_ASC
## ORDER_BY_DESC
string·enum
·default: "TB_PERIOD_LAST_1_DAY"required
Time period
period
## TB_PERIOD_LAST_1_DAY
## TB_PERIOD_LAST_1_WEEK
## TB_PERIOD_LAST_1_MONTH

06/02/26, 23.13Datasaham.io API
Page 18 of 56https://api.datasaham.io/swagger#description/-global-market
string·enum
·default: "MARKET_TYPE_ALL"required
Market type
marketType
## MARKET_TYPE_ALL
## MARKET_TYPE_REGULAR
## MARKET_TYPE_NEGOTIATED
## GET
## /api/market-detector/top-
## ...
## Shell Curl
1curl 'https:"#api.datasaham.io/api/market-detector/top-broker?sort=TB_SORT_BY_TOTAL_VALUE&order=ORDER_BY_DESC&period=TB_PERIOD_LAST_1_DAY&marketType=MARKET_TYPE_ALL' \
## 2  "$header 'x-api-key: ·····'
## Test Request
Retrieve list of top stocks by trading value,
volume, or frequency
## Query Parameters
Get top
stocks
stringrequired
Start date (YYYY-MM-DD)
startExample
stringrequired
End date (YYYY-MM-DD)
endExample

06/02/26, 23.13Datasaham.io API
Page 19 of 56https://api.datasaham.io/swagger#description/-global-market
string·enum
·default: "INVESTOR_TYPE_ALL"required
Investor type
investorType
## INVESTOR_TYPE_ALL
## INVESTOR_TYPE_DOMESTIC
## INVESTOR_TYPE_FOREIGN
string·enum
·default: "MARKET_TYPE_ALL"required
Market type
marketType
## MARKET_TYPE_ALL
## MARKET_TYPE_REGULAR
## MARKET_TYPE_NEGOTIATED
string·enum
·default: "VALUE_TYPE_TOTAL"required
Value type
valueType
## VALUE_TYPE_TOTAL
## VALUE_TYPE_BUY
## VALUE_TYPE_SELL
Any ofstring
page
string·numeric·default: 0
## GET
## /api/market-detector/top-
## ...
## Shell Curl
1curl 'https:"#api.datasaham.io/api/market-detector/top-stock?start=2026-01-05&end=2026-01-05&investorType=INVESTOR_TYPE_ALL&marketType=MARKET_TYPE_ALL&valueType=VALUE_TYPE_TOTAL' \
## 2  "$header 'x-api-key: ·····'
## Test Request
Get broker

06/02/26, 23.13Datasaham.io API
Page 20 of 56https://api.datasaham.io/swagger#description/-global-market
Retrieve broker trading summary for a specific
stock symbol
## Path Parameters
## Query Parameters
summary for
a stock
stringrequired
Stock symbol (e.g., BBCA)
symbolExamples
stringrequired
Start date (YYYY-MM-DD)
fromExample
stringrequired
End date (YYYY-MM-DD)
toExample
string·enum
·default: "TRANSACTION_TYPE_NET"required
Transaction type
transactionType
## TRANSACTION_TYPE_NET
## TRANSACTION_TYPE_GROSS
string·enum
·default: "MARKET_BOARD_ALL"required
Market board: ALL, REGULER (regular), NEGO
(negotiated), TUNAI (cash)
marketBoard
## MARKET_BOARD_ALL
## MARKET_BOARD_REGULER
## MARKET_BOARD_NEGO
## MARKET_BOARD_TUNAI

06/02/26, 23.13Datasaham.io API
Page 21 of 56https://api.datasaham.io/swagger#description/-global-market
string·enum
·default: "INVESTOR_TYPE_ALL"required
Investor type
investorType
## INVESTOR_TYPE_ALL
## INVESTOR_TYPE_DOMESTIC
## INVESTOR_TYPE_FOREIGN
Any ofstring
limit
string·numeric·default: 0
## GET
## /api/market-detector/brok
## ...
## Shell Curl
1curl 'https:"#api.datasaham.io/api/market-detector/broker-summary/BBCA?from=2026-01-02&to=2026-01-02&transactionType=TRANSACTION_TYPE_NET&marketBoard=MARKET_BOARD_ALL&investorType=INVESTOR_TYPE_ALL' \
## 2  "$header 'x-api-key: ·····'
## Test Request
Bandar/market maker analysis (accumulation,
distribution, smart money, pump & dump)
## Bandarmology
## Operations
GET/api/analysis/bandar/accumulation/{symbol}
GET/api/analysis/bandar/distribution/{symbol}
GET/api/analysis/bandar/smart-money/{symbol}
GET/api/analysis/bandar/pump-dump/{symbol}

06/02/26, 23.13Datasaham.io API
Page 22 of 56https://api.datasaham.io/swagger#description/-global-market
Detects if market makers (bandar) are
accumulating a stock based on broker
concentration, volume-price divergence, and
foreign flow patterns
## Path Parameters
## Query Parameters
## Bandar
## Accumulation
## Detector
string·min length:  1required
Stock symbol
symbolExamples
Any ofstring
days
string·numeric·default: 0
Jumlah hari untuk analisis. Nilai yang didukung: 7-
90 hari. Default: 30 hari.
## Examples
## GET
## /api/analysis/bandar/accu
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/analysis/bandar/accumulation/BUMI \
## 2  "$header 'x-api-key: ·····'
## Test Request

06/02/26, 23.13Datasaham.io API
Page 23 of 56https://api.datasaham.io/swagger#description/-global-market
Detects if market makers (bandar) are
distributing (selling) a stock - signals time to
exit
## Path Parameters
## Query Parameters
## Bandar
## Distribution
## Detector
string·min length:  1required
Stock symbol
symbolExamples
Any ofstring
days
string·numeric·default: 0
Jumlah hari untuk analisis. Nilai yang didukung: 7-
90 hari. Default: 30 hari.
## Examples
## GET
## /api/analysis/bandar/dist
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/analysis/bandar/distribution/BUMI \
## 2  "$header 'x-api-key: ·····'
## Test Request

06/02/26, 23.13Datasaham.io API
Page 24 of 56https://api.datasaham.io/swagger#description/-global-market
Tracks movement of smart money (institutions,
foreign investors, big brokers)
## Path Parameters
## Query Parameters
## Smart Money
## Flow Tracker
string·min length:  1required
Stock symbol
symbolExamples
Any ofstring
days
string·numeric·default: 0
Jumlah hari untuk analisis. Nilai yang didukung: 7-
90 hari. Default: 30 hari.
## Examples
## GET
## /api/analysis/bandar/smar
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/analysis/bandar/smart-money/BUMI \
## 2  "$header 'x-api-key: ·····'
## Test Request

06/02/26, 23.13Datasaham.io API
Page 25 of 56https://api.datasaham.io/swagger#description/-global-market
Detects pump & dump schemes to protect retail
investors from manipulation
## Path Parameters
## Query Parameters
## Pump &
## Dump
## Detector
string·min length:  1required
Stock symbol
symbolExamples
Any ofstring
days
string·numeric·default: 0
Jumlah hari untuk analisis pump/dump. Nilai yang
didukung: 7-30 hari (lebih pendek untuk deteksi
pump). Default: 14 hari.
## Examples
## GET
## /api/analysis/bandar/pump
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/analysis/bandar/pump-dump/BUMI \
## 2  "$header 'x-api-key: ·····'
## Test Request

06/02/26, 23.13Datasaham.io API
Page 26 of 56https://api.datasaham.io/swagger#description/-global-market
Retail opportunity finder (multibagger scanner,
breakout alerts, risk-reward calculator)
## Retail
## Opportunity
## Operations
GET/api/analysis/retail/multibagger/scan
GET/api/analysis/retail/breakout/alerts
GET/api/analysis/retail/risk-reward/{symbol}
GET/api/analysis/retail/sector-rotation
Scan for stocks with potential 2x-10x returns
based on multiple factors:
## Scoring Factors:
Technical Analysis (25%): Price position vs
52-week range, trend direction
Volume Analysis (20%): Volume surge,
unusual volume detection
Foreign Flow (25%): Net foreign
accumulation, consecutive buy days
Bandar Accumulation (30%): Market maker
activity, accumulation status
## Multibagger
## Candidate
## Scanner

06/02/26, 23.13Datasaham.io API
Page 27 of 56https://api.datasaham.io/swagger#description/-global-market
Output includes:
Multibagger score (0-100)
Potential return estimate (e.g., "2x-5x")
Entry zone with ideal and max prices
Target prices with probabilities
Risk level and stop loss recommendation
## Use Cases:
Find undervalued stocks with high growth
potential
Identify stocks being accumulated by
smart money
Screen for breakout candidates
## Query Parameters
Any ofstring
min_score
string·numeric·default: 0
Skor minimum multibagger (0-100). Semakin tinggi
skor, semakin potensial saham menjadi multibagger.
## Default: 50
## Examples
string
Filter berdasarkan nama sektor
sectorExamples
Any ofstring
max_results
string·numeric·default: 0
Jumlah maksimal hasil yang ditampilkan. Range: 1-
## 50. Default: 20
## Examples

06/02/26, 23.13Datasaham.io API
Page 28 of 56https://api.datasaham.io/swagger#description/-global-market
## GET
## /api/analysis/retail/mult
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/analysis/retail/multibagger/scan \
## 2  "$header 'x-api-key: ·····'
## Test Request
Real-time alerts for stocks that are breaking out
or about to break out.
## Alert Types:
VOLUME_BREAKOUT: High volume surge with
price movement
PRICE_BREAKOUT: Breaking above resistance
level
RESISTANCE_TEST: Approaching resistance
with momentum
SUPPORT_TEST: Testing support level with
volume
## Severity Levels:
HIGH: Strong breakout signal, immediate
action recommended
MEDIUM: Moderate signal, prepare for entry
LOW: Early signal, monitor closely
Output includes:
## Breakout
## Alert System

06/02/26, 23.13Datasaham.io API
Page 29 of 56https://api.datasaham.io/swagger#description/-global-market
Alert type and severity
Volume vs average comparison
Support and resistance levels
Breakout probability
Entry trigger conditions
Target and stop loss levels
## Use Cases:
Catch breakouts early for momentum
trading
Identify stocks with unusual volume activity
Get real-time trading signals
## GET
## /api/analysis/retail/brea
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/analysis/retail/breakout/alerts \
## 2  "$header 'x-api-key: ·····'
## Test Request
Calculate risk-reward ratio and position sizing
for a stock.
## Technical Analysis:
Risk-Reward
## Calculator

06/02/26, 23.13Datasaham.io API
Page 30 of 56https://api.datasaham.io/swagger#description/-global-market
Support and resistance levels (3 levels
each)
Pivot points (Classic formula)
ATR (Average True Range) for volatility
Risk-Reward Calculation:
Stop loss recommendation based on
support and ATR
Multiple target prices with probabilities
Risk-reward ratio for each target
## Position Sizing:
Maximum position as % of portfolio
Suggested number of shares
Total investment amount
Maximum loss amount
## Recommendation Levels:
## EXCELLENT_SETUP: R:R >= 3:1
## GOOD_SETUP: R:R >= 2:1
## FAIR_SETUP: R:R >= 1.5:1
## POOR_SETUP: R:R < 1.5:1
## Use Cases:
Plan entry and exit before trading
Calculate proper position size
Manage risk effectively
## Path Parameters
stringrequired
Stock symbol
symbolExamples

06/02/26, 23.13Datasaham.io API
Page 31 of 56https://api.datasaham.io/swagger#description/-global-market
## Query Parameters
Any ofstring
days
string·numeric·default: 0
Jumlah hari untuk analisis historis. Range: 7-90 hari.
Default: 30 hari
## Examples
Any ofstring
portfolio_size
string·numeric·default: 0
Ukuran portfolio dalam Rupiah untuk kalkulasi
position sizing. Minimum: Rp 1.000.000. Default: Rp
## 100.000.000
## Examples
Any ofstring
risk_percent
string·numeric·default: 0
Persentase risiko maksimal per trade. Range: 0.5-
## 10%. Default: 2%
## Examples
## GET
## /api/analysis/retail/risk
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/analysis/retail/risk-reward/BBCA \
## 2  "$header 'x-api-key: ·····'
## Test Request
## Sector
## Rotation

06/02/26, 23.13Datasaham.io API
Page 32 of 56https://api.datasaham.io/swagger#description/-global-market
Analyze sector rotation to identify hot and cold
sectors for timing entry/exit.
## Market Phase Detection:
EARLY_EXPANSION: Market starting to recover
LATE_EXPANSION: Market in full bull mode
EARLY_CONTRACTION: Market starting to
weaken
LATE_CONTRACTION: Market in full bear mode
NEUTRAL: No clear direction
## Sector Status:
LEADING: Strong momentum, outperforming
market
IMPROVING: Gaining momentum, potential
leader
WEAKENING: Losing momentum, potential
laggard
LAGGING: Weak momentum,
underperforming market
## Sector Recommendations:
OVERWEIGHT: Increase allocation to this
sector
NEUTRAL: Maintain current allocation
UNDERWEIGHT: Reduce allocation to this
sector
Output includes:
## Rotation
## Analyzer

06/02/26, 23.13Datasaham.io API
Page 33 of 56https://api.datasaham.io/swagger#description/-global-market
Hot sectors (momentum score >= 6)
Cold sectors (momentum score < 4)
All sectors with detailed metrics
Top stocks per sector
Foreign flow estimation
Market phase summary
## Use Cases:
Identify sectors to focus on
Time sector rotation trades
Understand market cycle position
## GET
## /api/analysis/retail/sect
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/analysis/retail/sector-rotation \
## 2  "$header 'x-api-key: ·····'
## Test Request

06/02/26, 23.13Datasaham.io API
Page 34 of 56https://api.datasaham.io/swagger#description/-global-market
Market sentiment analysis (retail vs bandar
sentiment, IPO momentum tracker)
## Market
## Sentiment
## Operations
GET/api/analysis/sentiment/{symbol}
GET/api/analysis/sentiment/ipo/momentum
Analyze sentiment divergence between retail
traders and institutional investors (bandar).
## Retail Sentiment Indicators:
frequency_score: Trading frequency (higher
= more retail activity)
small_lot_percentage: Percentage of small
lot transactions
fomo_score: Fear of missing out indicator
volume_participation: Retail volume
participation
## Retail Status:
Retail vs
## Bandar
## Sentiment
## Analysis

06/02/26, 23.13Datasaham.io API
Page 35 of 56https://api.datasaham.io/swagger#description/-global-market
EUPHORIC: Extreme bullish, high FOMO
(DANGER - potential top)
BULLISH: Positive sentiment
NEUTRAL: No clear direction
FEARFUL: Negative sentiment
PANIC: Extreme bearish (potential bottom)
## Bandar Sentiment Indicators:
top_broker_net_flow: Net flow from top 5
brokers
large_lot_percentage: Percentage of large
lot transactions
accumulation_score:
Accumulation/distribution score
foreign_flow: Foreign investor net flow
institutional_flow: Institutional
(Pemerintah) net flow
## Bandar Status:
ACCUMULATING: Smart money buying
HOLDING: Maintaining positions
NEUTRAL: No clear direction
DISTRIBUTING: Smart money selling
EXITING: Smart money exiting
## Divergence Types:

06/02/26, 23.13Datasaham.io API
Page 36 of 56https://api.datasaham.io/swagger#description/-global-market
## RETAIL_EUPHORIC_BANDAR_EXIT:  DANGER -
Retail FOMO while bandar exits
## RETAIL_PANIC_BANDAR_ACCUMULATE:
OPPORTUNITY - Retail panic while bandar
accumulates
ALIGNED_BULLISH: Both bullish - strong
momentum
ALIGNED_BEARISH: Both bearish - strong
downtrend
NEUTRAL: No significant divergence
## Use Cases:
Identify potential market tops (retail
euphoria + bandar exit)
Find buying opportunities (retail panic +
bandar accumulation)
Confirm trend strength (aligned sentiment)
## Path Parameters
## Query Parameters
stringrequired
Stock symbol
symbolExamples
Any ofstring
days
string·numeric·default: 0
Jumlah hari untuk analisis sentiment. Range: 1-30
hari. Default: 7 hari
## Examples
GET/api/analysis/sentiment/
## {
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/analysis/sentiment/BBCA \
## 2  "$header 'x-api-key: ·····'
## Test Request

06/02/26, 23.13Datasaham.io API
Page 37 of 56https://api.datasaham.io/swagger#description/-global-market
Track and analyze IPO momentum for trading
opportunities.
IPO Momentum Score (0-10): Based on
multiple factors:
Market condition (bullish/bearish)
Underwriter quality (Tier 1/2/3)
Price attractiveness
Offering size
## Underwriter Tiers:
TIER_1: Major securities (Mandiri, BCA,
Trimegah, Indo Premier, etc.)
TIER_2: Mid-tier securities (Henan Putihrai,
Sucor, Samuel, etc.)
TIER_3: Smaller securities
IPO Status:
UPCOMING: Not yet in offering period
OFFERING: Currently in offering period
LISTED: Already listed on exchange
PAST: Listed more than 30 days ago
## Strategy Recommendations:
## IPO
## Momentum
## Tracker

06/02/26, 23.13Datasaham.io API
Page 38 of 56https://api.datasaham.io/swagger#description/-global-market
STRONG_APPLY: High momentum, apply for
allocation
APPLY: Good momentum, consider applying
CONSIDER: Moderate momentum, evaluate
carefully
AVOID: Low momentum, high risk
Output includes:
Upcoming IPOs with momentum analysis
Recent IPOs (within 30 days) with
performance
Market sentiment assessment
Hot sectors identification
## Use Cases:
Identify high-potential IPOs for allocation
Track recent IPO performance
Time IPO trading strategies
## GET
## /api/analysis/sentiment/i
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/analysis/sentiment/ipo/momentum \
## 2  "$header 'x-api-key: ·····'
## Test Request

06/02/26, 23.13Datasaham.io API
Page 39 of 56https://api.datasaham.io/swagger#description/-global-market
Advanced analytics (correlation matrix, whale
transaction detector)
## Advanced
## Analytics
## Operations
GET/api/analysis/correlation
GET/api/analysis/whale-transactions/{symbol}
GET/api/analysis/insider-screening
GET/api/analysis/insider-net/{symbols}
GET/api/analysis/technical/{symbol}
GET/api/analysis/screener/multi-market
Calculate price correlation between multiple
stocks for portfolio diversification analysis.
## Correlation Values:
1.0: Perfect positive correlation (move
together)
0.0: No correlation (independent
movement)
-1.0: Perfect negative correlation (move
opposite)
## Correlation Strength:
## Correlation
## Matrix
## Calculator

06/02/26, 23.13Datasaham.io API
Page 40 of 56https://api.datasaham.io/swagger#description/-global-market
STRONG_POSITIVE: >= 0.7 (avoid holding
together)
MODERATE_POSITIVE: 0.3 to 0.7
WEAK: -0.3 to 0.3 (good for diversification)
MODERATE_NEGATIVE: -0.7 to -0.3
STRONG_NEGATIVE: <= -0.7 (good for hedging)
Output includes:
NxN correlation matrix
All unique pairs with correlation values
Insights: highly correlated, inversely
correlated, uncorrelated pairs
Per-symbol analysis with average
correlation
Trading implications and recommendations
## Use Cases:
Portfolio diversification analysis
Identify hedging opportunities
Sector correlation analysis
Risk management
## Query Parameters
stringrequired
Stock symbols dipisahkan koma untuk menghitung
korelasi antar saham
symbolsExamples
Any ofstring
period_days
string·numeric·default: 0
Jumlah hari untuk kalkulasi korelasi. Range: 7-365
hari. Default: 30 hari
## Examples

06/02/26, 23.13Datasaham.io API
Page 41 of 56https://api.datasaham.io/swagger#description/-global-market
GET/api/analysis/correlationShell Curl
1curl 'https:"#api.datasaham.io/api/analysis/correlation?symbols=BBCA%2CBBRI%2CBMRI%2CTLKM' \
## 2  "$header 'x-api-key: ·····'
## Test Request
Detect and analyze large institutional
transactions (whale activity).
## Whale Types:
MEGA_WHALE: >= 10x minimum lot threshold
LARGE_WHALE: >= 3x minimum lot threshold
MEDIUM_WHALE: >= minimum lot threshold
## Whale Activity Summary:
## Whale
## Transaction
## Detector

06/02/26, 23.13Datasaham.io API
Page 42 of 56https://api.datasaham.io/swagger#description/-global-market
Total whale buy/sell value
Net whale flow
Dominant action
## (ACCUMULATION/DISTRIBUTION/NEUTRA
## L)
Whale intensity
## (EXTREME/HIGH/MODERATE/LOW)
## Top Whale Brokers:
Broker code and type
(Asing/Lokal/Pemerintah)
Net value and lot
Whale score (0-10)
Action (ACCUMULATING/DISTRIBUTING)
## Prediction:
Short-term direction
## (BULLISH/BEARISH/NEUTRAL)
Confidence level (0-100%)
## Reasoning
## Alerts:
Mega whale transactions
Extreme activity warnings
Foreign flow alerts
Accumulation/Distribution signals
## Use Cases:

06/02/26, 23.13Datasaham.io API
Page 43 of 56https://api.datasaham.io/swagger#description/-global-market
Follow smart money
Detect institutional
accumulation/distribution
Time entry/exit based on whale activity
Monitor foreign investor flow
## Path Parameters
## Query Parameters
stringrequired
Stock symbol
symbolExamples
Any ofstring
min_lot
string·numeric·default: 0
Minimum lot threshold untuk deteksi transaksi
whale. Range: 100-10.000 lot. Default: 500 lot
## Examples
## GET
## /api/analysis/whale-trans
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/analysis/whale-transactions/BBCA \
## 2  "$header 'x-api-key: ·····'
## Test Request
Screen insider/major holder activity across all
stocks with various filters.
Flow yang direkomendasikan:
## Insider
## Screening
(Scriptless)

06/02/26, 23.13Datasaham.io API
Page 44 of 56https://api.datasaham.io/swagger#description/-global-market
## !"
Scan semua saham tanpa symbol untuk
cari insider activity
## $"
Filter by min_ownership >= 5% untuk cari
insider dengan kepemilikan signifikan
## %"
Filter by min_percentage >= 1% untuk cari
perubahan signifikan
## &"
Filter by source KSEI (data bulanan, lebih
akurat untuk akumulasi)
## '"
Filter by period (misal 2025-12 untuk
## Desember 2025)
## ("
Setelah dapat symbol, gunakan endpoint
/insider-net/:symbols untuk total akumulasi
## Filters:
symbols: Comma-separated symbols
(optional - kosongkan untuk scan semua)
min_percentage: Filter insider dengan
PERUBAHAN kepemilikan >= X%
min_ownership: Filter insider dengan
KEPEMILIKAN SAAT INI >= X% (misal 5
untuk >= 5%)
source_type: SOURCE_TYPE_KSEI (bulanan)
atau SOURCE_TYPE_IDX (harian)
action_type: ACTION_TYPE_BUY atau
## ACTION_TYPE_SELL
period: Format YYYY-MM atau YYYY-MM-
## DD
## Output:

06/02/26, 23.13Datasaham.io API
Page 45 of 56https://api.datasaham.io/swagger#description/-global-market
Summary: total movements, buy/sell count,
net value, dominant action
Top Symbols: saham dengan insider
activity terbesar
Top Insiders: insider dengan activity
terbesar
Movements: detail setiap transaksi
Alerts: notifikasi untuk activity signifikan
## Alert Types:
LARGE_ACCUMULATION: Akumulasi >= 1%
LARGE_DISTRIBUTION: Distribusi >= 1%
NEW_POSITION: Insider buka posisi baru
SIGNIFICANT_CHANGE: Kepemilikan >= 5%
## Use Cases:
Cari saham yang sedang diakumulasi
insider
Monitor aktivitas komisaris/direktur
Deteksi perubahan kepemilikan signifikan
Follow smart money dari data KSEI
## Query Parameters
string
Stock symbols dipisahkan koma (opsional - kosongkan
untuk scan semua saham)
symbolsExample
Any ofstring
min_percentage
string·numeric·default: 0
Filter insider dengan PERUBAHAN kepemilikan >=
## X%. Minimum: 0%
## Examples

06/02/26, 23.13Datasaham.io API
Page 46 of 56https://api.datasaham.io/swagger#description/-global-market
Any ofstring
min_ownership
string·numeric·default: 0
Filter insider dengan KEPEMILIKAN SAAT INI >= X%.
## Minimum: 0%
## Examples
string·enum
·default: "SOURCE_TYPE_UNSPECIFIED"
Filter by data source: KSEI (bulanan, lebih akurat) atau
IDX (harian)
source_type
## SOURCE_TYPE_UNSPECIFIED
## SOURCE_TYPE_IDX
## SOURCE_TYPE_KSEI
string·enum
·default: "ACTION_TYPE_UNSPECIFIED"
Filter by action type: BUY, SELL, CROSS (crossing),
TRANSFER, CORPACTION (corporate action)
action_type
## ACTION_TYPE_UNSPECIFIED
## ACTION_TYPE_BUY
## ACTION_TYPE_SELL
## ACTION_TYPE_CROSS
## ACTION_TYPE_TRANSFER
## ACTION_TYPE_CORPACTION
string
Filter by period (format: YYYY-MM atau YYYY-MM-
## DD)
periodExamples
Any ofstring
page
string·numeric·default: 0
Nomor halaman untuk pagination. Minimum: 1.
## Default: 1
## Examples

06/02/26, 23.13Datasaham.io API
Page 47 of 56https://api.datasaham.io/swagger#description/-global-market
Any ofstring
limit
string·numeric·default: 0
Jumlah item per halaman. Range: 1-100. Default:
## 100
## Examples
## GET
## /api/analysis/insider-scr
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/analysis/insider-screening \
## 2  "$header 'x-api-key: ·····'
## Test Request
Calculate total net buy/sell summary for
specific symbols.
Use Case: Setelah menemukan saham dari
insider-screening, gunakan endpoint ini untuk
melihat total akumulasi/distribusi per symbol.
## Filters:
## Insider Net
Buy/Sell
## Summary

06/02/26, 23.13Datasaham.io API
Page 48 of 56https://api.datasaham.io/swagger#description/-global-market
date_start: Filter dari tanggal (YYYY-MM-
## DD)
date_end: Filter sampai tanggal (YYYY-MM-
## DD)
## Output:
Per symbol: total buy, total sell, net shares,
net value
Per insider: detail aktivitas setiap insider
Overall: total net value dan dominant action
## Example:
## !"
Dari insider-screening, dapat BUMI, ADRO,
BBCA yang ada insider activity
## $"
Panggil /insider-net/BUMI,ADRO,BBCA?
date_start=2025-11-01&date_end=2025-
## 11-30
## %"
Lihat mana yang net buy terbesar di bulan
## November
## Path Parameters
## Query Parameters
stringrequired
Comma-separated stock symbols untuk hitung total
net buy/sell
symbolsExample
string
## ·^\d{4}-\d{2}-\d{2}$
Filter by start date (YYYY-MM-DD)
date_start
## Example
string
## ·^\d{4}-\d{2}-\d{2}$
Filter by end date (YYYY-MM-DD)
date_endExample

06/02/26, 23.13Datasaham.io API
Page 49 of 56https://api.datasaham.io/swagger#description/-global-market
## GET
## /api/analysis/insider-net
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/analysis/insider-net/BBCA,BUMI,ADRO \
## 2  "$header 'x-api-key: ·····'
## Test Request
Comprehensive technical analysis with multiple
indicators.
## Date Range Options:
Use from and to to specify exact date
range (recommended for accurate
analysis)
Or use period to get last N candles from
today
If from and to are provided, period is
ignored
Available Indicators (use 'indicators' query
param):
## Technical
## Analyst

06/02/26, 23.13Datasaham.io API
Page 50 of 56https://api.datasaham.io/swagger#description/-global-market
sma: Simple Moving Average (5, 10, 20, 50,
## 200)
ema: Exponential Moving Average (5, 10, 20,
## 50, 200)
rsi: Relative Strength Index (14 period)
macd: MACD with signal line and histogram
stochastic: Stochastic Oscillator (%K, %D)
bollinger: Bollinger Bands with %B
atr: Average True Range
obv: On-Balance Volume
vwap: Volume Weighted Average Price
trend: Trend analysis (short/medium/long
term)
support_resistance: Support & resistance
levels
signal: Trading signal recommendation
all: All indicators (default)
## Example Usage:
All indicators with date range:
/technical/BBCA?from=2026-01-01&to=2026-01-
## 30
Only RSI & MACD: /technical/BBCA?
indicators=rsi,macd
Moving averages & trend: /technical/BBCA?
indicators=sma,ema,trend
## Timeframes:
daily: Daily candles (default)
15m, 30m, 1h, 2h, 3h, 4h: Intraday candles
## Trading Signal:

06/02/26, 23.13Datasaham.io API
Page 51 of 56https://api.datasaham.io/swagger#description/-global-market
Action: STRONG_BUY, BUY, HOLD, SELL,
## STRONG_SELL
Confidence level (0-100%)
Detailed reasoning
## Path Parameters
## Query Parameters
stringrequired
Stock symbol (e.g., BBCA)
symbolExample
string·enum·default: "daily"
Chart timeframe (default: daily)
timeframe
daily
## 15m
## 30m
## 1h
## 2h
## 3h
## 4h
Any ofstring
period
string·numeric·default: 0
Number of candles to analyze (default: 100).
Ignored if from/to are provided.
string
## ·^\d{4}-\d{2}-\d{2}$
Start date for analysis (YYYY-MM-DD). If provided
with "to", period is ignored.
fromExamples
string
## ·^\d{4}-\d{2}-\d{2}$
End date for analysis (YYYY-MM-DD). If provided with
"from", period is ignored.
toExamples

06/02/26, 23.13Datasaham.io API
Page 52 of 56https://api.datasaham.io/swagger#description/-global-market
string
Comma-separated indicators to calculate. Options:
sma,ema,rsi,macd,stochastic,bollinger,atr,obv,vwap,tr
end,support_resistance,signal. Default: all
indicatorsExamples
GET/api/analysis/technical/
## {
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/analysis/technical/BBCA \
## 2  "$header 'x-api-key: ·····'
## Test Request
Screen IDX stocks based on global market
factors (commodities, forex).
## Commodity Exposure Filter:
Multi-Market
## Screener

06/02/26, 23.13Datasaham.io API
Page 53 of 56https://api.datasaham.io/swagger#description/-global-market
Coal: ADRO, PTBA, ITMG, BUMI
Oil: MEDC, ELSA
Gold: ANTM, MDKA
Nickel: ANTM, INCO, NCKL
## CPO: AALI, LSIP
Tin: TINS
Copper: TPIA
## Forex Exposure Filter:
exporter: Stocks that benefit from IDR
weakening (ADRO, PTBA, ANTM, INCO,
## AALI)
importer: Stocks that benefit from IDR
strengthening (ASII, UNVR, ICBP)
## Output:
Stock list with global factor impact analysis
Commodity impact:
positive/negative/neutral based on
commodity price movement
Forex impact: positive/negative/neutral
based on USD/IDR movement
Overall score combining all factors
Global context: current commodity prices
and forex rates
## Use Cases:
Find stocks benefiting from commodity
rally
Screen exporters when IDR is weakening
Portfolio construction based on global
factors

06/02/26, 23.13Datasaham.io API
Page 54 of 56https://api.datasaham.io/swagger#description/-global-market
## Query Parameters
string
Filter by commodity exposure (comma-separated):
Coal, Oil, Gold, Nickel, CPO, Tin, Copper
commodityExposureExamples
string·enum·default: "all"
Filter by forex exposure type
forexExposure
exporter
importer
all
Any ofstring
minPrice
string·numeric·default: 0
Minimum stock price filter
Any ofstring
maxPrice
string·numeric·default: 0
Maximum stock price filter
Any ofstring
minVolume
string·numeric·default: 0
Minimum volume filter
## GET
## /api/analysis/screener/mu
## ...
## Shell Curl
1curl https:"#api.datasaham.io/api/analysis/screener/multi-market \
## 2  "$header 'x-api-key: ·····'
## Test Request

06/02/26, 23.13Datasaham.io API
Page 55 of 56https://api.datasaham.io/swagger#description/-global-market
Emiten/company information and data
## Emiten
## Operations
GET/api/emiten/{symbol}/info
GET/api/emiten/{symbol}/orderbook
GET/api/emiten/running-trade
GET/api/emiten/tradebook-chart
GET/api/emiten/{symbol}/historical-summary
GET/api/emiten/{symbol}/broker-trade-chart
GET/api/emiten/{symbol}/seasonality
GET/api/emiten/{symbol}/profile
GET/api/emiten/{symbol}/subsidiary
GET/api/emiten/{symbol}/keystats
GET/api/emiten/insider
GET/api/emiten/{symbol}/insider
GET/api/emiten/fundachart
GET/api/emiten/fundachart/metrics
GET/api/emiten/{symbol}/financials
GET/api/emiten/{symbol}/profile/holding-composition
GET/api/emiten/{symbol}/foreign-ownership
## Show More

06/02/26, 23.13Datasaham.io API
Page 56 of 56https://api.datasaham.io/swagger#description/-global-market
Experimental features - may change without
notice.
## BETA
## Operations
GET/api/beta/insights/{symbol}
GET/api/beta/earnings/{symbol}
GET/api/beta/equities/{symbol}
GET/api/beta/keyratios/{symbol}
## Show More