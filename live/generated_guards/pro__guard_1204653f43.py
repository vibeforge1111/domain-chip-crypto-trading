def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extremes for high-confidence entries.

    Args:
        features: Dict with keys like bb_pct_b, vwap_deviation, stoch_k, stoch_d, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Only allow longs at extreme lower band, shorts at extreme upper band
    if prediction == "long" and bb_pct_b >= 0.05:
        return "skip"
    if prediction == "short" and bb_pct_b <= 0.95:
        return "skip"
    
    return prediction