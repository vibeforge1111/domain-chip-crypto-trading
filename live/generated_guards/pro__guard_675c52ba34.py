def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using bb_pct_b and stoch_k."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Extreme zones: both indicators aligned at boundaries
    overbought = bb_pct_b > 0.92 and stoch_k > 85 and stoch_d > 80
    oversold = bb_pct_b < 0.08 and stoch_k < 15 and stoch_d < 20
    
    # Reject longs at overbought, shorts at oversold
    if prediction == "long" and overbought:
        return "skip"
    if prediction == "short" and oversold:
        return "skip"
    
    return prediction