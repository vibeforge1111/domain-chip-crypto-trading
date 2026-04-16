def guard(features: dict, prediction: str) -> str:
    """Reject trades where macd_histogram contradicts momentum direction."""
    macd = features.get("macd_histogram", 0)
    
    if prediction == "long" and macd < 0:
        return "skip"
    if prediction == "short" and macd > 0:
        return "skip"
    
    return prediction