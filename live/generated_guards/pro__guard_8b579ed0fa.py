def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d, vwap_deviation, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Skip long signals when both BB and Stoch confirm overbought extremes
    if prediction == 'long' and bb_pct > 0.9 and stoch > 80:
        return 'skip'
    
    # Skip short signals when both BB and Stoch confirm oversold extremes
    if prediction == 'short' and bb_pct < 0.1 and stoch < 20:
        return 'skip'
    
    return prediction