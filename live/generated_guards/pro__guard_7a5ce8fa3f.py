def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation: require 2+ signals to agree with direction."""
    if prediction not in ("long", "short"):
        return prediction
    
    bullish = sum([
        features.get("vwap_deviation", 0) > 0,
        features.get("bb_pct_b", 0.5) > 0.5,
        features.get("macd_histogram", 0) > 0,
        features.get("obv_slope", 0) > 0,
    ])
    bearish = sum([
        features.get("vwap_deviation", 0) < 0,
        features.get("bb_pct_b", 0.5) < 0.5,
        features.get("macd_histogram", 0) < 0,
        features.get("obv_slope", 0) < 0,
    ])
    
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction