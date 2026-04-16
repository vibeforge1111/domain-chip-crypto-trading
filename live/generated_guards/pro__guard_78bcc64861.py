def guard(features: dict, prediction: str) -> str:
    """Filter trades when price is not at Bollinger Band extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # For longs, require price near lower band (oversold)
    if prediction == "long" and bb_pct_b >= 0.05:
        return "skip"
    
    # For shorts, require price near upper band (overbought)
    if prediction == "short" and bb_pct_b <= 0.95:
        return "skip"
    
    return prediction