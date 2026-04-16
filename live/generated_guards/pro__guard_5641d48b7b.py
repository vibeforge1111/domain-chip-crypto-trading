def guard(features: dict, prediction: str) -> str:
    """Filter trades that go against the broader 2h trend."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    
    # Align with broader trend: longs need bullish 2h, shorts need bearish 2h
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction