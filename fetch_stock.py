#!/usr/bin/env python3
"""
股票數據獲取腳本 - 使用 yfinance
支援多種數據源：yfinance, Yahoo Finance API, Alpha Vantage
"""

import json
import time
from datetime import datetime
import urllib.request
import re

# 嘗試匯入 yfinance
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("yfinance not available, using alternative method")

def fetch_stock_data_yfinance(symbols):
    """使用 yfinance 獲取股票數據"""
    if not YFINANCE_AVAILABLE:
        return None
    
    results = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            # 獲取即時報價
            info = ticker.info
            results[symbol] = {
                'symbol': symbol,
                'name': info.get('shortName', symbol),
                'price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'change': info.get('regularMarketChange', 0),
                'changePercent': info.get('regularMarketChangePercent', 0),
                'open': info.get('regularMarketOpen', 0),
                'high': info.get('regularMarketDayHigh', 0),
                'low': info.get('regularMarketDayLow', 0),
                'volume': info.get('regularMarketVolume', 0),
                'previousClose': info.get('regularMarketPreviousClose', 0),
                'marketCap': info.get('marketCap', 0),
                'timestamp': datetime.now().isoformat()
            }
            print(f"Fetched {symbol}: ${results[symbol]['price']}")
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            results[symbol] = {'symbol': symbol, 'error': str(e)}
        time.sleep(0.5)  # 避免請求過快
    
    return results

def fetch_stock_data_api(symbols):
    """使用免費 API 獲取股票數據（無需 API Key）"""
    results = {}
    
    for symbol in symbols:
        try:
            # 使用 stockprices.dev 免費 API
            url = f"https://api.stockprices.dev/v1/stock/{symbol}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                results[symbol] = {
                    'symbol': symbol,
                    'price': data.get('price', 0),
                    'change': data.get('change', 0),
                    'changePercent': data.get('changePercent', 0),
                    'high': data.get('high', 0),
                    'low': data.get('low', 0),
                    'open': data.get('open', 0),
                    'volume': data.get('volume', 0),
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"API error for {symbol}: {e}")
            # 備用方案：使用Yahoo Finance 間接數據
            results[symbol] = fallback_yahoo_finance(symbol)
        
        time.sleep(0.3)
    
    return results

def fallback_yahoo_finance(symbol):
    """備用方案：直接解析 Yahoo Finance 頁面"""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            result = data['chart']['result'][0]
            meta = result['meta']
            return {
                'symbol': symbol,
                'price': meta.get('regularMarketPrice', 0),
                'change': meta.get('regularMarketChange', 0),
                'changePercent': meta.get('regularMarketChangePercent', 0),
                'open': meta.get('regularMarketOpen', 0),
                'high': meta.get('regularMarketDayHigh', 0),
                'low': meta.get('regularMarketDayLow', 0),
                'volume': meta.get('regularMarketVolume', 0),
                'previousClose': meta.get('chartPreviousClose', 0),
                'timestamp': datetime.now().isoformat()
            }
    except Exception as e:
        print(f"Yahoo Finance fallback error for {symbol}: {e}")
        return {'symbol': symbol, 'error': str(e)}

def fetch_historical_data(symbol, period='1mo', interval='1d'):
    """獲取歷史K線數據"""
    if not YFINANCE_AVAILABLE:
        return fetch_historical_api(symbol, period, interval)
    
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)
        
        data = []
        for date, row in hist.iterrows():
            data.append({
                'date': date.isoformat(),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'volume': int(row['Volume'])
            })
        return data
    except Exception as e:
        print(f"Error fetching historical data for {symbol}: {e}")
        return []

def fetch_historical_api(symbol, period='1mo', interval='1d'):
    """使用 API 獲取歷史數據"""
    try:
        period_map = {'1d': '1d', '5d': '5d', '1mo': '1mo', '3mo': '3mo', '6mo': '6mo', '1y': '1y'}
        range_param = period_map.get(period, '1mo')
        
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval={interval}&range={range_param}"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            result = data['chart']['result'][0]
            
            timestamps = result['timestamp']
            quote = result['indicators']['quote'][0]
            
            data = []
            for i, ts in enumerate(timestamps):
                data.append({
                    'date': datetime.fromtimestamp(ts).isoformat(),
                    'open': quote['open'][i],
                    'high': quote['high'][i],
                    'low': quote['low'][i],
                    'close': quote['close'][i],
                    'volume': quote['volume'][i]
                })
            return data
    except Exception as e:
        print(f"Historical API error for {symbol}: {e}")
        return []

if __name__ == '__main__':
    # 測試數據獲取
    test_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']
    print("=== Testing yfinance ===")
    data = fetch_stock_data_yfinance(test_symbols)
    print(json.dumps(data, indent=2))
