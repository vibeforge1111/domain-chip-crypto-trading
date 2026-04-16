def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys including bb_pct_b, stoch_k, stoch_d, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # High-confidence entries only at Bollinger Band extremes
    # Lower band (< 0.05): valid for long entries
    # Upper band (> 0.95): valid for short entries
    if bb_pct_b < 0.05 and prediction == "long":
        return prediction
    if bb_pct_b > 0.95 and prediction == "short":
        return prediction
    
    return "skip"