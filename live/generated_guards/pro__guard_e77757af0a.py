def guard(features: dict, prediction: str) -> str:
    """Filter false compression breakouts using multiple timeframe confirmation."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    macd_histogram = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # True compression: low bb_width AND low atr_ratio (genuine squeeze)
    true_compression = (bb_width < 0.5 and atr_ratio < 0.8)
    
    # False compression: tight bands but high volatility (deceptive setup)
    false_compression = (bb_width < 0.4 and atr_ratio > 1.1)
    
    if false_compression:
        return "skip"
    
    if true_compression:
        # Stochastic alignment (not extreme)
        if not (20 < stoch_k < 80 and 20 < stoch_d < 80):
            return "skip"
        # MACD histogram not bearish for longs, not bullish for shorts
        if prediction == "long" and macd_histogram < -0.0005:
            return "skip"
        if prediction == "short" and macd_histogram > 0.0005:
            return "skip"
        # RSI 2H in valid range (not extreme)
        if not (25 < rsi_2h < 75):
            return "skip"
        # VWAP within reasonable range
        if abs(vwap_deviation) > 0.015:
            return "skip"
    
    return prediction