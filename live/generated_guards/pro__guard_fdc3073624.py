def guard(features: dict, prediction: str) -> str:
    """Filter trades when MACD histogram shows momentum deceleration near crossover."""
    macd = features.get("macd_histogram", 0)
    
    # Skip long if histogram is positive but near zero (bullish momentum weakening)
    if prediction == "long" and 0 < macd < 0.0003:
        return "skip"
    
    # Skip short if histogram is negative but near zero (bearish momentum weakening)
    if prediction == "short" and -0.0003 < macd < 0:
        return "skip"
    
    return prediction