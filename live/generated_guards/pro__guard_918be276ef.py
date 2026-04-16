def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard with multiple confirmations."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    bb_pct = features.get("bb_pct_b", 0.5)
    obv_slope = features.get("obv_slope", 0)
    
    # Stochastic crossover zone: k above d for longs, k below d for shorts
    # Both should be in 20-80 range (avoiding overbought/oversold extremes)
    stoch_valid = 20 <= stoch_k <= 80 and 20 <= stoch_d <= 80
    
    if prediction == "long":
        # Bullish crossover: stoch_k above stoch_d
        if stoch_k <= stoch_d and stoch_valid:
            return "skip"
        # Confirm price not too far below VWAP
        if vwap_dev < -0.005:
            return "skip"
        # Confirm OBV not strongly negative
        if obv_slope < -1:
            return "skip"
            
    elif prediction == "short":
        # Bearish crossover: stoch_k below stoch_d
        if stoch_k >= stoch_d and stoch_valid:
            return "skip"
        # Confirm price not too far above VWAP
        if vwap_dev > 0.005:
            return "skip"
        # Confirm not in strong accumulation
        if obv_slope > 2:
            return "skip"
            
    return prediction