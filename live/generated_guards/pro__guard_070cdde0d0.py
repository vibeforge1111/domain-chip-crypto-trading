def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    macd_hist = features.get('macd_histogram', 0)
    
    # Momentum deceleration filter - skip if MACD histogram near zero (weak/converging momentum)
    if abs(macd_hist) < 0.0001:
        return "skip"
    
    # For longs, require bullish momentum (positive histogram)
    if prediction == "long" and macd_hist < 0:
        return "skip"
    
    # For shorts, require bearish momentum (negative histogram)
    if prediction == "short" and macd_hist > 0:
        return "skip"
    
    return prediction