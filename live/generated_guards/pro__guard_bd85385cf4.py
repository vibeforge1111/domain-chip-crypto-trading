def guard(features: dict, prediction: str) -> str:
    """Filter trades using 2-hour RSI to align with broader trend."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Long entries require bullish broader trend (rsi_2h above 45)
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    
    # Short entries require bearish broader trend (rsi_2h below 55)
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction