def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish signals
    bullish_count = 0
    # Count bearish signals  
    bearish_count = 0
    
    # Stochastic confirmation (both in oversold/overbought territory)
    if features['stoch_k'] < 30 and features['stoch_d'] < 30:
        bullish_count += 1
    elif features['stoch_k'] > 70 and features['stoch_d'] > 70:
        bearish_count += 1
    
    # Bollinger Band position
    if features['bb_pct_b'] < 0.25:
        bullish_count += 1
    elif features['bb_pct_b'] > 0.75:
        bearish_count += 1
    
    # VWAP deviation (below = bullish for longs, above = bearish for shorts)
    if features['vwap_deviation'] < -0.002:
        bullish_count += 1
    elif features['vwap_deviation'] > 0.002:
        bearish_count += 1
    
    # MACD histogram direction
    if features['macd_histogram'] > 0:
        bullish_count += 1
    elif features['macd_histogram'] < 0:
        bearish_count += 1
    
    # RSI 2h context
    if features['rsi_2h'] < 45:
        bullish_count += 1
    elif features['rsi_2h'] > 55:
        bearish_count += 1
    
    # OBV slope
    if features['obv_slope'] > 0:
        bullish_count += 1
    elif features['obv_slope'] < 0:
        bearish_count += 1
    
    # Require at least 2 signals to confirm direction
    if prediction == "long" and bullish_count < 2:
        return "skip"
    elif prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction