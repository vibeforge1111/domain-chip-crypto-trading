def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard - requires 2+ signals to agree."""
    
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # Stochastic: oversold (<30) bullish, overbought (>70) bearish
    if features.get("stoch_k", 50) < 30:
        bullish_count += 1
    elif features.get("stoch_k", 50) > 70:
        bearish_count += 1
    
    # Bollinger position: near lower band (<0.2) bullish, near upper band (>0.8) bearish
    if features.get("bb_pct_b", 0.5) < 0.2:
        bullish_count += 1
    elif features.get("bb_pct_b", 0.5) > 0.8:
        bearish_count += 1
    
    # VWAP deviation: below VWAP (negative) bullish, above (positive) bearish
    if features.get("vwap_deviation", 0) < -0.01:
        bullish_count += 1
    elif features.get("vwap_deviation", 0) > 0.01:
        bearish_count += 1
    
    # MACD histogram: positive bullish, negative bearish
    if features.get("macd_histogram", 0) > 0:
        bullish_count += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish_count += 1
    
    # RSI 2h context: oversold (<40) bullish, overbought (>60) bearish
    if features.get("rsi_2h", 50) < 40:
        bullish_count += 1
    elif features.get("rsi_2h", 50) > 60:
        bearish_count += 1
    
    # Require at least 2 confirming signals
    if prediction == "long":
        return "skip" if bullish_count < 2 else prediction
    elif prediction == "short":
        return "skip" if bearish_count < 2 else prediction
    
    return prediction