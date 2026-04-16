def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Reject long signals at overbought extremes (both indicators confirm)
    if prediction == 'long' and bb_pct_b > 0.85 and stoch_k > 80:
        return 'skip'
    
    # Reject short signals at oversold extremes (both indicators confirm)
    if prediction == 'short' and bb_pct_b < 0.15 and stoch_k < 20:
        return 'skip'
    
    return prediction