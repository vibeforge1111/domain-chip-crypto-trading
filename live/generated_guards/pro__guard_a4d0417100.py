def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d, vwap_deviation, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Skip longs when overbought: both bb_pct_b and stoch_k confirm extreme
    if prediction == 'long' and bb > 0.85 and stoch > 80:
        return "skip"
    
    # Skip shorts when oversold: both bb_pct_b and stoch_k confirm extreme
    if prediction == 'short' and bb < 0.15 and stoch < 20:
        return "skip"
    
    return prediction