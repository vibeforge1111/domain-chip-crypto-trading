def guard(features: dict, prediction: str) -> str:
    """Reject trades where momentum contradicts direction or is weakening."""
    macd = features.get("macd_histogram", 0)
    stoch = features.get("stoch_k", 50)
    
    if prediction == "long" and (macd < 0 or stoch > 80):
        return "skip"
    if prediction == "short" and (macd > 0 or stoch < 20):
        return "skip"
    return prediction