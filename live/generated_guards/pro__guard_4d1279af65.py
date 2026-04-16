def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d, vwap_deviation, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when overbought (bb_pct_b > 0.85 and stoch_k > 80)
    if prediction == "long" and bb_pct_b > 0.85 and stoch_k > 80:
        return "skip"
    
    # Skip shorts when oversold (bb_pct_b < 0.15 and stoch_k < 20)
    if prediction == "short" and bb_pct_b < 0.15 and stoch_k < 20:
        return "skip"
    
    # Skip longs when 2h RSI confirms overbought
    if prediction == "long" and bb_pct_b > 0.80 and rsi_2h > 70:
        return "skip"
    
    # Skip shorts when 2h RSI confirms oversold
    if prediction == "short" and bb_pct_b < 0.20 and rsi_2h < 30:
        return "skip"
    
    return prediction