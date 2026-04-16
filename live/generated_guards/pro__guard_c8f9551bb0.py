def guard(features: dict, prediction: str) -> str:
    """Custom guard function using rsi_2h to align with broader trend."""
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Align with broader trend
    if prediction == "long":
        # Reject if broader timeframe is bearish
        if rsi_2h < 45:
            return "skip"
        # Reject if overbought on both timeframes
        if stoch_k > 85 and rsi_2h > 60:
            return "skip"
        # Reject if price far above VWAP (potential reversal)
        if vwap_dev > 0.02:
            return "skip"
    
    elif prediction == "short":
        # Reject if broader timeframe is bullish
        if rsi_2h > 55:
            return "skip"
        # Reject if oversold on both timeframes
        if stoch_k < 15 and rsi_2h < 40:
            return "skip"
        # Reject if price far below VWAP (potential bounce)
        if vwap_dev < -0.02:
            return "skip"
    
    # Reject extreme BB positions regardless of direction
    if bb_pct_b > 0.95 or bb_pct_b < 0.05:
        return "skip"
    
    return prediction