def guard(features: dict, prediction: str) -> str:
    """Filter trades where MACD histogram shows momentum deceleration."""
    if prediction == "skip":
        return prediction
    
    macd = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip longs: MACD turning negative signals bearish momentum shift
    if prediction == "long" and macd < 0:
        return "skip"
    
    # Skip shorts: MACD turning positive signals bullish momentum shift
    if prediction == "short" and macd > 0:
        return "skip"
    
    # Double-filter: skip longs with stoch overbought + negative MACD
    if prediction == "long" and stoch_k > 70 and macd < 0:
        return "skip"
    
    return prediction