def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    bb_pct = features.get("bb_pct_b", 0.5)
    
    # Detect bullish crossover: stoch_k crosses above stoch_d in oversold
    bullish_cross = stoch_k > stoch_d and stoch_k < 30
    # Detect bearish crossover: stoch_k crosses below stoch_d in overbought
    bearish_cross = stoch_k < stoch_d and stoch_k > 70
    
    # Long entry: bullish cross with pullback (below VWAP and lower BB half)
    if prediction == "long":
        if not (bullish_cross and vwap_dev < 0 and bb_pct < 0.3):
            return "skip"
    
    # Short entry: bearish cross with rally (above VWAP and upper BB half)
    if prediction == "short":
        if not (bearish_cross and vwap_dev > 0 and bb_pct > 0.7):
            return "skip"
    
    return prediction