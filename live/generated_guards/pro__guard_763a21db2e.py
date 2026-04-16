def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum is decelerating using MACD histogram."""
    macd = features.get('macd_histogram', 0)
    rsi_14 = features.get('rsi_14', 50)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if momentum is decelerating (histogram near zero)
    if abs(macd) < 0.0003:
        return "skip"
    
    # Skip if overextended with weakening momentum
    if (stoch_k > 80 or stoch_k < 20) and abs(macd) < 0.0005:
        return "skip"
    
    return prediction