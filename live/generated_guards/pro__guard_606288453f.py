def guard(features: dict, prediction: str) -> str:
    """Filter trades to only allow entries at BB extreme zones."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    # Only allow trades at BB extremes (<0.05 oversold for longs, >0.95 overbought for shorts)
    if prediction == 'long' and bb_pct_b >= 0.05:
        return 'skip'
    if prediction == 'short' and bb_pct_b <= 0.95:
        return 'skip'
    return prediction