def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, vwap_deviation, stoch_k, stoch_d, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # RSI confirmation: not extreme
    if features.get("rsi_2h", 50) < 70:
        confirmations += 1
    
    # Stochastic confirmation: not overbought
    if features.get("stoch_k", 50) < 80:
        confirmations += 1
    
    # VWAP confirmation: price above VWAP for long
    if features.get("vwap_deviation", 0) > 0:
        confirmations += 1
    
    # OBV slope confirmation: positive momentum
    if features.get("obv_slope", 0) > 0:
        confirmations += 1
    
    # MACD histogram confirmation: positive histogram
    if features.get("macd_histogram", 0) > 0:
        confirmations += 1
    
    # Require at least 2 confirmations
    if confirmations < 2:
        return "skip"
    
    return prediction