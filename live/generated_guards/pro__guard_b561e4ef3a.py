def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with market features
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    obv_slope = features.get("obv_slope", 0)
    
    # Long only when near lower band AND stoch oversold
    if prediction == "long" and not (bb_pct < 0.05 and stoch_k < 25):
        return "skip"
    
    # Short only when near upper band AND stoch overbought
    if prediction == "short" and not (bb_pct > 0.95 and stoch_k > 75):
        return "skip"
    
    return prediction