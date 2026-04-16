def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    long_signals = [
        features.get("stoch_k", 50) > 30,
        features.get("vwap_deviation", 0) > 0,
        features.get("macd_histogram", 0) > 0,
        features.get("obv_slope", 0) > 0,
        features.get("bb_pct_b", 0.5) > 0.35,
    ]
    
    short_signals = [
        features.get("stoch_k", 50) < 70,
        features.get("vwap_deviation", 0) < 0,
        features.get("macd_histogram", 0) < 0,
        features.get("obv_slope", 0) < 0,
        features.get("bb_pct_b", 0.5) < 0.65,
    ]
    
    if prediction == "long" and sum(long_signals) < 2:
        return "skip"
    elif prediction == "short" and sum(short_signals) < 2:
        return "skip"
    
    return prediction