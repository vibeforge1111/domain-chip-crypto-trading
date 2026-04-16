def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    macd_histogram = features.get("macd_histogram", 0)
    
    # Reject trades when momentum is decelerating (histogram near zero)
    # macd_histogram normalized by price: small values mean weak momentum
    if abs(macd_histogram) < 0.0005:
        return "skip"
    
    return prediction