def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    macd_hist = features.get('macd_histogram', 0)
    
    # Skip if momentum is decelerating (histogram near zero or negative)
    if macd_hist < 0.00005:
        return "skip"
    
    return prediction