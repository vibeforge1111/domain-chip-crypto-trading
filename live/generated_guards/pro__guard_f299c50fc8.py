def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    # Detect momentum deceleration: macd_histogram positive but weakening (low value)
    # This suggests bullish momentum is fading, bad for longs
    if prediction == "long" and features.get("macd_histogram", 0) < 0.0005:
        return "skip"
    
    # For shorts: macd_histogram negative but strengthening (high/less negative value)
    if prediction == "short" and features.get("macd_histogram", 0) > -0.0005:
        return "skip"
    
    # Additional momentum check: RSI 2h overbought/oversold divergence
    if features.get("rsi_2h", 50) > 70 and prediction == "long":
        return "skip"
    if features.get("rsi_2h", 50) < 30 and prediction == "short":
        return "skip"
    
    return prediction