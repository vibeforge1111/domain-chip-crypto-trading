def guard(features: dict, prediction: str) -> str:
    """Filter trades that contradict the broader 2-hour trend."""
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long" and rsi_2h < 42:
        return "skip"
    if prediction == "short" and rsi_2h > 58:
        return "skip"
    
    return prediction