def guard(features: dict, prediction: str) -> str:
    """Filter trades using bb_pct_b extremes with stochastic confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Extreme lower band (<0.05): reject shorts, require oversold stoch
    if bb_pct_b < 0.05:
        if prediction == "short":
            return "skip"
        if stoch_k > 20:
            return "skip"
    
    # Extreme upper band (>0.95): reject longs, require overbought stoch
    if bb_pct_b > 0.95:
        if prediction == "long":
            return "skip"
        if stoch_k < 80:
            return "skip"
    
    return prediction