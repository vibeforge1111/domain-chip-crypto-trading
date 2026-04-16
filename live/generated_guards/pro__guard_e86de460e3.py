def guard(features: dict, prediction: str) -> str:
    """Filter trades when MACD histogram indicates momentum deceleration."""
    if prediction == "skip":
        return prediction
    
    macd_hist = features.get("macd_histogram", 0)
    abs_hist = abs(macd_hist)
    
    # Skip if momentum is negligible (histogram near zero)
    if abs_hist < 0.0001:
        return "skip"
    
    # For long: histogram should be positive and meaningful
    if prediction == "long" and macd_hist < 0.0002:
        return "skip"
    
    # For short: histogram should be negative and meaningful
    if prediction == "short" and macd_hist > -0.0002:
        return "skip"
    
    return prediction