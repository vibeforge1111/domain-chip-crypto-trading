def guard(features: dict, prediction: str) -> str:
    """Filter trades using BB extreme zones with confirming indicators."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # High-confidence zones: BB extremes with confirming indicators
    if bb_pct_b < 0.05 and stoch_k < 25:
        return prediction
    if bb_pct_b > 0.95 and stoch_k > 75:
        return prediction
    
    return "skip"