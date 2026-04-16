def guard(features: dict, prediction: str) -> str:
    """Filter trades not aligned with 2-hour broader trend."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    
    # Align long entries with broader 2h uptrend
    if prediction == "long" and rsi_2h < 50:
        return "skip"
    
    # Align short entries with broader 2h downtrend
    if prediction == "short" and rsi_2h > 50:
        return "skip"
    
    return prediction