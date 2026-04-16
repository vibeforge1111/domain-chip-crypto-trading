def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extremes for high-confidence entries."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    rsi_14 = features.get("rsi_14", 50)
    
    # High-confidence long: bb_pct_b in lower 5% and RSI confirmation
    if prediction == "long" and not (bb_pct_b < 0.05 and rsi_14 < 40):
        return "skip"
    
    # High-confidence short: bb_pct_b in upper 5% and RSI confirmation
    if prediction == "short" and not (bb_pct_b > 0.95 and rsi_14 > 60):
        return "skip"
    
    return prediction