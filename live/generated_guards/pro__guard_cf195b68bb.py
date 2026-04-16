def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Reject longs when both Bollinger Bands AND Stochastic are in overbought territory
    if prediction == "long" and bb_pct_b > 0.88 and stoch_k > 80:
        return "skip"
    
    # Reject shorts when both Bollinger Bands AND Stochastic are in oversold territory
    if prediction == "short" and bb_pct_b < 0.12 and stoch_k < 20:
        return "skip"
    
    # Additional filter: reject when stochastic is diverging from BB position
    if prediction == "long" and stoch_k < 30 and bb_pct_b > 0.7:
        return "skip"
    
    if prediction == "short" and stoch_k > 70 and bb_pct_b < 0.3:
        return "skip"
    
    return prediction