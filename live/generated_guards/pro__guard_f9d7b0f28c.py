def guard(features: dict, prediction: str) -> str:
    """Filter trades during compression to detect true vs false breakouts."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.5)
    stoch_k = features.get('stoch_k', 50)
    macd_histogram = features.get('macd_histogram', 0)
    
    # True compression: both volatility measures are low
    is_compression = atr_ratio < 0.7 and bb_width < 0.3
    
    if is_compression and prediction in ("long", "short"):
        # For longs: require stoch recovering from oversold and positive momentum
        if prediction == "long" and (stoch_k < 30 or macd_histogram < 0):
            return "skip"
        # For shorts: require stoch declining from overbought and negative momentum
        if prediction == "short" and (stoch_k > 70 or macd_histogram > 0):
            return "skip"
    
    return prediction