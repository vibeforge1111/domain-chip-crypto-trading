def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extreme positions."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # High-confidence entry zones: bb_pct_b extreme (<0.05 or >0.95)
    bb_extreme = bb_pct_b < 0.05 or bb_pct_b > 0.95
    
    if not bb_extreme:
        return "skip"
    
    # Additional confirmation: stochastic not in oversold/overbought reversal zone
    # (too extreme stoch at extreme BB suggests reversal risk)
    stoch_extreme = stoch_k < 20 or stoch_k > 80
    
    if stoch_extreme:
        return "skip"
    
    return prediction