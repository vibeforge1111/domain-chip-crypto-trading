def guard(features: dict, prediction: str) -> str:
    """Guard: filter signals not at bb_pct_b extremes (<0.05 or >0.95)."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Long signals only valid at extreme low (oversold near lower band)
    if prediction == "long" and bb_pct_b >= 0.05:
        return "skip"
    # Short signals only valid at extreme high (overbought near upper band)
    if prediction == "short" and bb_pct_b <= 0.95:
        return "skip"
    
    return prediction