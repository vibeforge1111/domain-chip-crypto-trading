def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    mh = features.get("macd_histogram", 0)
    sk = features.get("stoch_k", 50)
    
    # Skip longs if momentum is decelerating (negative histogram) and overbought
    if prediction == "long" and mh < -0.0003 and sk > 75:
        return "skip"
    
    # Skip shorts if momentum is still building (positive histogram) and oversold
    if prediction == "short" and mh > 0.0003 and sk < 25:
        return "skip"
    
    return prediction