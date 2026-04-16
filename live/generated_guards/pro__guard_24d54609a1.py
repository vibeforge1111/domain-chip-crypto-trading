def guard(features: dict, prediction: str) -> str:
    """Filter trades to only allow high-confidence entries at Bollinger Band extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # High-confidence long: near lower band (bb_pct_b < 0.05)
    if prediction == "long" and bb_pct_b < 0.05:
        return prediction
    # High-confidence short: near upper band (bb_pct_b > 0.95)
    if prediction == "short" and bb_pct_b > 0.95:
        return prediction
    
    return "skip"