def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend using rsi_2h."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # For longs, require 2h RSI to confirm bullish broad trend
    if prediction == "long" and rsi_2h < 48:
        return "skip"
    
    # For shorts, require 2h RSI to confirm bearish broad trend
    if prediction == "short" and rsi_2h > 52:
        return "skip"
    
    return prediction