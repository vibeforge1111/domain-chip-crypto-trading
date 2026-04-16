def guard(features: dict, prediction: str) -> str:
    """Filter signals with momentum divergence or extreme volatility conditions."""
    rsi = features.get('rsi_14', 50)
    stoch = features.get('stoch_k', 50)
    macd = features.get('macd_histogram', 0)
    obv = features.get('obv_slope', 0)
    
    # Bearish divergence: RSI overbought but momentum fading (low MACD, declining OBV)
    if rsi > 68 and macd < -0.0003 and obv < 0:
        return "skip"
    
    # Bullish divergence: RSI oversold but momentum building (high MACD, rising OBV)
    if rsi < 32 and macd > 0.0003 and obv > 0:
        return "skip"
    
    # Choppy market: RSI neutral but conflicting momentum signals
    if 40 <= rsi <= 60 and macd * obv < 0:
        return "skip"
    
    return prediction