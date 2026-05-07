#!/usr/bin/env python3
"""
技術分析指標計算模組
包含：MA、RSI、MACD、KDJ、Bollinger Bands
"""

import json
from datetime import datetime

def calculate_sma(prices, period):
    """簡單移動平均線 (Simple Moving Average)"""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period

def calculate_ema(prices, period):
    """指數移動平均線 (Exponential Moving Average)"""
    if len(prices) < period:
        return None
    
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period
    
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    
    return ema

def calculate_rsi(prices, period=14):
    """相對強弱指數 (Relative Strength Index)"""
    if len(prices) < period + 1:
        return None
    
    changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    
    gains = [c if c > 0 else 0 for c in changes]
    losses = [-c if c < 0 else 0 for c in changes]
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return round(rsi, 2)

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """MACD (Moving Average Convergence Divergence)"""
    if len(prices) < slow:
        return None, None, None
    
    # 計算 EMA
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    
    if ema_fast is None or ema_slow is None:
        return None, None, None
    
    macd_line = ema_fast - ema_slow
    
    # 計算信號線 (Signal Line) - MACD 的 EMA
    # 需要歷史 MACD 值來計算
    macd_values = []
    for i in range(slow, len(prices)):
        ef = calculate_ema(prices[:i+1], fast)
        es = calculate_ema(prices[:i+1], slow)
        if ef and es:
            macd_values.append(ef - es)
    
    if len(macd_values) < signal:
        signal_line = macd_line
    else:
        signal_line = calculate_ema(macd_values, signal)
    
    histogram = macd_line - signal_line if signal_line else 0
    
    return round(macd_line, 4), round(signal_line, 4), round(histogram, 4)

def calculate_kdj(highs, lows, closes, period=9, k_period=3, d_period=3):
    """KDJ 隨機指標"""
    if len(closes) < period:
        return None, None, None
    
    # 計算 RSV (Raw Stochastic Value)
    recent_highs = highs[-period:]
    recent_lows = lows[-period:]
    recent_closes = closes[-period:]
    
    highest_high = max(recent_highs)
    lowest_low = min(recent_lows)
    latest_close = recent_closes[-1]
    
    if highest_high == lowest_low:
        rsv = 50
    else:
        rsv = (latest_close - lowest_low) / (highest_high - lowest_low) * 100
    
    # 計算 K 值
    k = 2/3 * 50 + 1/3 * rsv if len(closes) == period else (2/3 * 50 + 1/3 * rsv)
    
    # 計算 D 值
    d = 2/3 * 50 + 1/3 * k
    
    # 計算 J 值
    j = 3 * k - 2 * d
    
    return round(k, 2), round(d, 2), round(j, 2)

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    """布林帶 (Bollinger Bands)"""
    if len(prices) < period:
        return None, None, None
    
    recent_prices = prices[-period:]
    sma = sum(recent_prices) / period
    
    variance = sum((p - sma) ** 2 for p in recent_prices) / period
    std = variance ** 0.5
    
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    
    return round(upper_band, 2), round(sma, 2), round(lower_band, 2)

def calculate_all_indicators(historical_data):
    """計算所有技術指標"""
    if not historical_data or len(historical_data) < 30:
        return {}
    
    closes = [d['close'] for d in historical_data]
    highs = [d['high'] for d in historical_data]
    lows = [d['low'] for d in historical_data]
    volumes = [d['volume'] for d in historical_data]
    
    indicators = {
        'ma5': calculate_sma(closes, 5),
        'ma10': calculate_sma(closes, 10),
        'ma20': calculate_sma(closes, 20),
        'ma60': calculate_sma(closes, 60) if len(closes) >= 60 else None,
        'ema12': calculate_ema(closes, 12),
        'ema26': calculate_ema(closes, 26),
        'rsi': calculate_rsi(closes, 14),
        'macd': {},
        'kdj': {},
        'bollinger': {}
    }
    
    # MACD
    macd_line, signal_line, histogram = calculate_macd(closes)
    indicators['macd'] = {
        'line': macd_line,
        'signal': signal_line,
        'histogram': histogram
    }
    
    # KDJ
    k, d, j = calculate_kdj(highs, lows, closes)
    indicators['kdj'] = {'k': k, 'd': d, 'j': j}
    
    # Bollinger Bands
    upper, middle, lower = calculate_bollinger_bands(closes)
    indicators['bollinger'] = {'upper': upper, 'middle': middle, 'lower': lower}
    
    # 成交量移動平均
    if len(volumes) >= 5:
        indicators['volume_ma5'] = sum(volumes[-5:]) / 5
    else:
        indicators['volume_ma5'] = None
    
    return indicators

def format_indicators_for_display(indicators):
    """格式化指標數據用於顯示"""
    formatted = {}
    
    for key, value in indicators.items():
        if isinstance(value, dict):
            formatted[key] = value
        elif isinstance(value, float):
            formatted[key] = round(value, 2) if value else None
        else:
            formatted[key] = value
    
    return formatted

if __name__ == '__main__':
    # 測試指標計算
    test_data = []
    import random
    base_price = 100
    
    for i in range(60):
        base_price += random.uniform(-2, 2)
        test_data.append({
            'date': f'2024-01-{i+1:02d}',
            'open': base_price - 0.5,
            'high': base_price + random.uniform(0, 2),
            'low': base_price - random.uniform(0, 2),
            'close': base_price,
            'volume': random.randint(1000000, 5000000)
        })
    
    indicators = calculate_all_indicators(test_data)
    print("=== Technical Indicators ===")
    print(json.dumps(format_indicators_for_display(indicators), indent=2))
