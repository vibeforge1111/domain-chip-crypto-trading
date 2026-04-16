def guard(features: dict, prediction: str) -> str:
    """Filter trades using extreme Bollinger Band positions with confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    if prediction == "long":
        # Only long at extreme lower band with oversold confirmation
        if bb_pct_b > 0.10:
            return "skip"
        if stoch_k > 30:
            return "skip"
        if vwap_dev > 0.002:
            return "skip"
    
    elif prediction == "short":
        # Only short at extreme upper band with overbought confirmation
        if bb_pct_b < 0.90:
            return "skip"
        if stoch_k < 70:
            return "skip"
        if vwap_dev < -0.002:
            return "skip"
    
    return prediction