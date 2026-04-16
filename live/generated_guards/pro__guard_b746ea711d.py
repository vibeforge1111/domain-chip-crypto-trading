def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like rsi_2h, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    rsi_2h = features.get("rsi_2h", 50)
    
    # For long signals, require 2h RSI to be above 50 (bullish broader trend)
    if prediction == "long" and rsi_2h < 50:
        return "skip"
    
    # For short signals, require 2h RSI to be below 50 (bearish broader trend)
    if prediction == "short" and rsi_2h > 50:
        return "skip"
    
    return prediction