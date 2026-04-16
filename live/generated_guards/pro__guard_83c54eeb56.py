def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum is decelerating (macd_histogram near zero)."""
    macd_histogram = features.get('macd_histogram', 0)
    
    # Reject long when histogram near zero or negative (momentum weakening)
    if prediction == 'long' and macd_histogram < 0.0003:
        return 'skip'
    
    # Reject short when histogram near zero or positive (momentum weakening)
    if prediction == 'short' and macd_histogram > -0.0003:
        return 'skip'
    
    return prediction