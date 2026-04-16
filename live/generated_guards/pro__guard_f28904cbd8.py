def guard(features: dict, prediction: str) -> str:
    """Filter trades using extreme Bollinger Band positions as entry zones."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    if prediction == "long":
        # Only allow longs at lower band extremes with confirming factors
        if bb_pct_b >= 0.05 or stoch_k >= 20 or vwap_dev >= 0:
            return "skip"
    elif prediction == "short":
        # Only allow shorts at upper band extremes with confirming factors
        if bb_pct_b <= 0.95 or stoch_k <= 80 or vwap_dev <= 0:
            return "skip"
    
    return prediction