def guard(features: dict, prediction: str) -> str:
    """Reject entries where momentum is decelerating (histogram near zero)."""
    macd_histogram = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # Skip longs when macd_histogram is near zero (exhausted upward momentum)
    if prediction == "long" and abs(macd_histogram) < 0.001:
        return "skip"
    
    # Skip shorts when macd_histogram is near zero (exhausted downward momentum)
    if prediction == "short" and abs(macd_histogram) < 0.001:
        return "skip"
    
    return prediction