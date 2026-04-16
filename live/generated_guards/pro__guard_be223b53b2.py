def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs when overbought extreme (stoch > 80 AND near upper band)
    if prediction == 'long' and stoch_k > 80 and bb_pct_b > 0.9:
        return 'skip'
    
    # Skip shorts when oversold extreme (stoch < 20 AND near lower band)
    if prediction == 'short' and stoch_k < 20 and bb_pct_b < 0.1:
        return 'skip'
    
    return prediction