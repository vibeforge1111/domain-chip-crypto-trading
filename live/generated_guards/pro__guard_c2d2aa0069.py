def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, vwap_deviation, stoch_k, stoch_d, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # High-confidence long: at lower band extreme (<0.05) AND oversold stochastic
    if prediction == "long" and not (bb_pct_b < 0.05 and stoch_k < 20):
        return "skip"
    
    # High-confidence short: at upper band extreme (>0.95) AND overbought stochastic
    if prediction == "short" and not (bb_pct_b > 0.95 and stoch_k > 80):
        return "skip"
    
    return prediction