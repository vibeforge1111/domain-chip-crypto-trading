def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like macd_histogram, bb_pct_b, vwap_deviation, stoch_k, stoch_d, obv_slope, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    macd = features.get('macd_histogram', 0)
    
    # Momentum deceleration check: reject longs with negative macd, shorts with positive macd
    if prediction == 'long' and macd < 0:
        return 'skip'
    if prediction == 'short' and macd > 0:
        return 'skip'
    
    return prediction