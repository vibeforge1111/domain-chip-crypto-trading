def guard(features: dict, prediction: str) -> str:
    """Filter trades where MACD histogram shows momentum deceleration against direction."""
    if prediction == "skip":
        return prediction
    
    macd = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # For longs: skip if momentum fading AND wider timeframe shows weakness
    if prediction == "long" and macd < -0.0005 and rsi_2h < 45:
        return "skip"
    
    # For shorts: skip if momentum fading AND wider timeframe shows strength
    if prediction == "short" and macd > 0.0005 and rsi_2h > 55:
        return "skip"
    
    return prediction