def guard(features: dict, prediction: str) -> str:
    """Filter trades when MACD histogram shows momentum deceleration near extremes."""
    macd = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Detect momentum flattening (deceleration) with extreme stochastic
    momentum_flat = abs(macd) < 0.0001
    stoch_extreme = stoch_k > 80 or stoch_k < 20
    bb_extreme = bb_pct_b > 0.95 or bb_pct_b < 0.05
    
    if momentum_flat and stoch_extreme and bb_extreme:
        return "skip"
    
    # Additional: reject if going long with bearish macd and overbought stoch
    if prediction == "long" and macd < -0.00005 and stoch_k > 75:
        return "skip"
    
    # Additional: reject if going short with bullish macd and oversold stoch
    if prediction == "short" and macd > 0.00005 and stoch_k < 25:
        return "skip"
    
    return prediction