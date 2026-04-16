def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using VWAP deviation."""
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip if price too close to fair value (no edge)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Skip long if overbought on both timeframes
    if prediction == "long" and stoch_k > 80 and stoch_d > 80:
        return "skip"
    
    # Skip short if oversold on both timeframes
    if prediction == "short" and stoch_k < 20 and stoch_d < 20:
        return "skip"
    
    # Skip long if 2h RSI extremely overbought
    if prediction == "long" and rsi_2h > 85:
        return "skip"
    
    # Skip short if 2h RSI extremely oversold
    if prediction == "short" and rsi_2h < 15:
        return "skip"
    
    return prediction