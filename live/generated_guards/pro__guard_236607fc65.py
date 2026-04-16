def guard(features: dict, prediction: str) -> str:
    """Filter trades that are too close to fair value (VWAP)."""
    vwap_deviation = features.get('vwap_deviation', 0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip if too close to fair value (< 0.4% from VWAP)
    if abs(vwap_deviation) < 0.004:
        return "skip"
    
    # Skip if in middle of Bollinger Bands (no extension)
    if 0.35 < bb_pct_b < 0.65:
        return "skip"
    
    # Skip if stochastic extreme AND wider RSI confirms reversal risk
    if (stoch_k > 85 or stoch_k < 15) and (rsi_2h > 70 or rsi_2h < 30):
        return "skip"
    
    return prediction