def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram shows momentum deceleration against direction."""
    macd_histogram = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # For longs: skip if momentum is bearish (negative histogram)
    if prediction == "long" and macd_histogram < 0:
        return "skip"
    
    # For shorts: skip if momentum is bullish (positive histogram)
    if prediction == "short" and macd_histogram > 0:
        return "skip"
    
    return prediction