def guard(features: dict, prediction: str) -> str:
    """Reject entries when momentum is decelerating (negative macd_histogram)."""
    macd_histogram = features.get("macd_histogram", 0)
    
    # Skip if momentum is clearly decelerating
    if macd_histogram < -0.001:
        return "skip"
    
    return prediction