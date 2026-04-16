def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram shows momentum deceleration."""
    macd = features.get('macd_histogram', 0)
    
    # Skip if momentum is clearly decelerating (negative histogram)
    if macd < 0:
        return "skip"
    
    return prediction