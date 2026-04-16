def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish signals
    bullish = (features.get('vwap_deviation', 0) > 0) + (features.get('obv_slope', 0) > 0) + (features.get('macd_histogram', 0) > 0)
    
    # Count bearish signals
    bearish = (features.get('vwap_deviation', 0) < 0) + (features.get('obv_slope', 0) < 0) + (features.get('macd_histogram', 0) < 0)
    
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction