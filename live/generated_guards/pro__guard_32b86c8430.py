def guard(features: dict, prediction: str) -> str:
    """Custom guard using bb_pct_b extremes for high-confidence entries."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # High-confidence entry zones: BB extremes
    if bb_pct_b < 0.05:
        # Lower band extreme: reject if not oversold or too far below VWAP
        if stoch_k > 30 or vwap_dev < -0.01:
            return "skip"
        return prediction
    elif bb_pct_b > 0.95:
        # Upper band extreme: reject if not overbought or too far above VWAP
        if stoch_k < 70 or vwap_dev > 0.01:
            return "skip"
        return prediction
    
    # Reject trades not at BB extremes
    return "skip"