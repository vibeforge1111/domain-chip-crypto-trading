def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_deviation = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Only allow trades at BB extremes for high-confidence entries
    if bb_pct_b > 0.05 and bb_pct_b < 0.95:
        return "skip"
    
    # Reject longs if RSI_2h is overbought
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    
    # Reject shorts if RSI_2h is oversold
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    
    # Reject longs if price above VWAP (not below)
    if prediction == "long" and vwap_deviation >= 0:
        return "skip"
    
    # Reject shorts if price below VWAP (not above)
    if prediction == "short" and vwap_deviation <= 0:
        return "skip"
    
    return prediction