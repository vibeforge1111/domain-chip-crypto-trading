def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Only accept trades at extreme Bollinger Band positions
    # <0.05: price at lower band (bullish reversal zone) → valid for longs
    # >0.95: price at upper band (bearish reversal zone) → valid for shorts
    if bb_pct_b < 0.05:
        return prediction
    elif bb_pct_b > 0.95:
        return prediction
    else:
        return "skip"