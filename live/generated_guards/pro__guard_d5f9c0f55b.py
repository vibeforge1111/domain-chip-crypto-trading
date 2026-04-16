def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d, vwap_deviation, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    obv_slope = features.get("obv_slope", 0)
    
    # Skip long signals at extreme overbought with price above VWAP and weakening volume
    if prediction == "long" and bb_pct > 0.85 and stoch_k > 80 and vwap_dev > 0.005 and obv_slope < 0:
        return "skip"
    
    # Skip short signals at extreme oversold with price below VWAP and strengthening volume
    if prediction == "short" and bb_pct < 0.15 and stoch_k < 20 and vwap_dev < -0.005 and obv_slope > 0:
        return "skip"
    
    return prediction