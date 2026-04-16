def guard(features: dict, prediction: str) -> str:
    """Filter trades where 2h RSI doesn't align with the broader trend direction."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    
    # For longs, require 2h RSI above 52 (bullish broader trend)
    # For shorts, require 2h RSI below 48 (bearish broader trend)
    if prediction == "long" and rsi_2h < 52:
        return "skip"
    if prediction == "short" and rsi_2h > 48:
        return "skip"
    
    return prediction