def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish signals
    bullish_count = 0
    bearish_count = 0
    
    # BB position: above 0.5 bullish, below 0.5 bearish
    if features.get("bb_pct_b", 0.5) > 0.5:
        bullish_count += 1
    else:
        bearish_count += 1
    
    # VWAP: positive deviation bullish
    if features.get("vwap_deviation", 0) > 0:
        bullish_count += 1
    else:
        bearish_count += 1
    
    # Stochastic: oversold (< 20) bullish, overbought (> 80) bearish
    stoch_k = features.get("stoch_k", 50)
    if stoch_k < 30:
        bullish_count += 1
    elif stoch_k > 70:
        bearish_count += 1
    
    # OBV slope: positive bullish
    if features.get("obv_slope", 0) > 0:
        bullish_count += 1
    else:
        bearish_count += 1
    
    # MACD histogram: positive bullish
    if features.get("macd_histogram", 0) > 0:
        bullish_count += 1
    else:
        bearish_count += 1
    
    # RSI 2h: above 50 bullish
    if features.get("rsi_2h", 50) > 50:
        bullish_count += 1
    else:
        bearish_count += 1
    
    # Require 2+ signals to agree with prediction direction
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction