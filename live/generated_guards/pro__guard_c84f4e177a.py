def guard(features: dict, prediction: str) -> str:
    """Guard using BB extreme zones (<0.05 or >0.95) as high-confidence entries."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Only allow trades at BB extremes for high confidence
    if not (bb_pct_b < 0.05 or bb_pct_b > 0.95):
        return "skip"
    
    # Validate with VWAP alignment
    if prediction == "long" and vwap_deviation < -0.01:
        return "skip"
    if prediction == "short" and vwap_deviation > 0.01:
        return "skip"
    
    # Stochastic confirmation - avoid overbought/oversold exhaustion
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    # Filter with 2h RSI for trend context
    if prediction == "long" and rsi_2h > 75:
        return "skip"
    if prediction == "short" and rsi_2h < 25:
        return "skip"
    
    return prediction