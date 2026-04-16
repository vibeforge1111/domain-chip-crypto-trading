def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, vwap_deviation, stoch_k, stoch_d, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # Skip longs when bb_pct_b > 0.95 (price at upper band extreme - overbought, likely reversal down)
    if prediction == 'long' and bb_pct_b > 0.95:
        return 'skip'
    
    # Skip shorts when bb_pct_b < 0.05 (price at lower band extreme - oversold, likely reversal up)
    if prediction == 'short' and bb_pct_b < 0.05:
        return 'skip'
    
    return prediction