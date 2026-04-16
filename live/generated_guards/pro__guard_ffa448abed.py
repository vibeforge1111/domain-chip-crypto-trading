def guard(features: dict, prediction: str) -> str:
    """Guard using Bollinger Band extreme positions (<0.05 or >0.95) for high-confidence entries."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # High-confidence entry zones at Bollinger Band extremes
    lower_extreme = bb_pct_b < 0.05
    upper_extreme = bb_pct_b > 0.95
    
    # Stochastic confirmation for entries
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # VWAP deviation for additional confirmation
    vwap_dev = features.get('vwap_deviation', 0)
    
    if prediction == "long":
        # Accept long: at lower BB extreme with stoch confirming oversold, or stoch fully oversold
        if lower_extreme or (stoch_k < 20 and stoch_d < 25):
            return prediction
        # Also accept if deeply oversold with VWAP below
        if stoch_k < 15 and vwap_dev < -0.005:
            return prediction
        return "skip"
    
    if prediction == "short":
        # Accept short: at upper BB extreme with stoch confirming overbought, or stoch fully overbought
        if upper_extreme or (stoch_k > 80 and stoch_d > 75):
            return prediction
        # Also accept if deeply overbought with VWAP above
        if stoch_k > 85 and vwap_dev > 0.005:
            return prediction
        return "skip"
    
    return prediction