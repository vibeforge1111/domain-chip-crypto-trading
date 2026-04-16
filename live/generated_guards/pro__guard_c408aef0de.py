def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using Bollinger Band extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    rsi_14 = features.get("rsi_14", 50)
    macd_histogram = features.get("macd_histogram", 0)
    
    # Only allow trades at BB extremes (<0.05 or >0.95)
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    # Validate momentum alignment with prediction
    if prediction == "long" and macd_histogram < 0:
        return "skip"
    if prediction == "short" and macd_histogram > 0:
        return "skip"
    
    return prediction