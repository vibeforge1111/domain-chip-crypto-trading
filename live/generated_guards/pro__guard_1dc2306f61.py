def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    if prediction == "long":
        bullish = sum([
            features.get("rsi_14", 50) < 70,
            features.get("stoch_k", 50) < 75,
            features.get("vwap_deviation", 0) > 0,
            features.get("macd_histogram", 0) > 0,
            features.get("obv_slope", 0) > 0,
            features.get("rsi_2h", 50) < 65
        ])
        return prediction if bullish >= 2 else "skip"
    
    if prediction == "short":
        bearish = sum([
            features.get("rsi_14", 50) > 30,
            features.get("stoch_k", 50) > 25,
            features.get("vwap_deviation", 0) < 0,
            features.get("macd_histogram", 0) < 0,
            features.get("obv_slope", 0) < 0,
            features.get("rsi_2h", 50) > 35
        ])
        return prediction if bearish >= 2 else "skip"
    
    return prediction