def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compressions using ATR, BB, and momentum indicators."""
    if prediction == "skip":
        return prediction
    
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # True compression: low volatility AND tight bands
    in_compression = atr_ratio < 0.7 and bb_width < 0.8
    
    if in_compression:
        # False compression signals: extreme BB position AND divergent stochastics
        extreme_bb = bb_pct_b < 0.15 or bb_pct_b > 0.85
        stoch_divergent = abs(stoch_k - stoch_d) > 15
        
        if extreme_bb and stoch_divergent:
            return "skip"
        
        # False compression: broader timeframe RSI contradicts direction
        if prediction == "long" and rsi_2h < 35:
            return "skip"
        if prediction == "short" and rsi_2h > 65:
            return "skip"
    
    return prediction