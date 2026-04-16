def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using Bollinger Band extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Filter longs: only allow when price near lower band (<0.05)
    if prediction == "long" and bb_pct_b >= 0.05:
        return "skip"
    
    # Filter shorts: only allow when price near upper band (>0.95)
    if prediction == "short" and bb_pct_b <= 0.95:
        return "skip"
    
    return prediction