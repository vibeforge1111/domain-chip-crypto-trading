def guard(features: dict, prediction: str) -> str:
    """Skip trades where momentum is diverging from the predicted direction."""
    macd_hist = features.get("macd_histogram", 0)
    
    if prediction == "long" and macd_hist < -0.0002:
        return "skip"
    if prediction == "short" and macd_hist > 0.0002:
        return "skip"
    
    return prediction