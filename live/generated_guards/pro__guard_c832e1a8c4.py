def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes with confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # High-confidence entry zones: bb_pct_b extremes
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    # For long signals, require stoch oversold confirmation
    if prediction == "long" and stoch_k >= 30:
        return "skip"
    
    # For short signals, require stoch overbought confirmation
    if prediction == "short" and stoch_k <= 70:
        return "skip"
    
    return prediction