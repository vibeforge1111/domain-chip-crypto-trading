def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram shows momentum against trade direction."""
    hist = features.get("macd_histogram", 0)
    
    if prediction == "long" and hist < -0.0001:
        return "skip"
    elif prediction == "short" and hist > 0.0001:
        return "skip"
    
    return prediction