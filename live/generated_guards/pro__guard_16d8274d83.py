def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    obv_slope = features.get("obv_slope", 0)
    
    long_signals = 0
    short_signals = 0
    
    # BB position confirmation
    if bb_pct_b < 0.3:
        long_signals += 1
    if bb_pct_b > 0.7:
        short_signals += 1
    
    # VWAP deviation confirmation
    if vwap_dev < -0.005:
        long_signals += 1
    if vwap_dev > 0.005:
        short_signals += 1
    
    # Stochastic confirmation
    if stoch_k < 25 and stoch_d < 25:
        long_signals += 1
    if stoch_k > 75 and stoch_d > 75:
        short_signals += 1
    
    # Higher timeframe RSI filter
    if rsi_2h < 40:
        long_signals += 1
    if rsi_2h > 60:
        short_signals += 1
    
    # OBV slope confirmation
    if obv_slope > 0:
        long_signals += 1
    if obv_slope < 0:
        short_signals += 1
    
    # Require 2+ indicators to agree
    if prediction == "long" and long_signals < 2:
        return "skip"
    if prediction == "short" and short_signals < 2:
        return "skip"
    
    return prediction