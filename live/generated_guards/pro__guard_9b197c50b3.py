def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    macd_histogram = features.get("macd_histogram", 0)
    obv_slope = features.get("obv_slope", 0)
    
    confirm_count = 0
    
    if prediction == "long":
        confirm_count += vwap_deviation > 0
        confirm_count += stoch_k < 80
        confirm_count += rsi_2h < 70
        confirm_count += macd_histogram > 0
        confirm_count += obv_slope > 0
        confirm_count += bb_pct_b < 0.95
    elif prediction == "short":
        confirm_count += vwap_deviation < 0
        confirm_count += stoch_k > 20
        confirm_count += rsi_2h > 30
        confirm_count += macd_histogram < 0
        confirm_count += obv_slope < 0
        confirm_count += bb_pct_b > 0.05
    
    return "skip" if confirm_count < 2 else prediction