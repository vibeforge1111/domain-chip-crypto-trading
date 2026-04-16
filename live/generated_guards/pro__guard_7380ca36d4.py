def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with market features
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    macd_hist = features.get('macd_histogram', 0)
    
    # Skip longs with negative macd (momentum decelerating)
    if prediction == 'long' and macd_hist < -0.00005:
        return 'skip'
    
    # Skip shorts with positive macd (momentum accelerating against us)
    if prediction == 'short' and macd_hist > 0.00005:
        return 'skip'
    
    return prediction