def guard(features: dict, prediction: str) -> str:
    """Filter false compression signals using BB width, ATR ratio, and momentum."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    stoch_k = features.get('stoch_k', 50)
    macd_histogram = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # True compression: BB width and ATR ratio both low (they agree)
    is_compressed = bb_width < 0.15 and atr_ratio < 0.85
    
    if is_compressed:
        # Skip long when overbought with bearish momentum
        if stoch_k > 80 and macd_histogram < 0 and prediction == "long":
            return "skip"
        # Skip short when oversold with bullish momentum
        if stoch_k < 20 and macd_histogram > 0 and prediction == "short":
            return "skip"
    
    return prediction