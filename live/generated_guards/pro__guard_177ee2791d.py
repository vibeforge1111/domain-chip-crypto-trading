def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like vwap_deviation, bb_pct_b, stoch_k, stoch_d, rsi_2h, macd_histogram, obv_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    # Skip if price too close to VWAP (within 0.2% = indecisive zone)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    
    # Skip if extreme stochastic readings
    stoch_k = features.get('stoch_k', 50)
    if stoch_k > 85 or stoch_k < 15:
        return "skip"
    
    return prediction