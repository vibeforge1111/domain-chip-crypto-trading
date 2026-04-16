def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    macd_hist = features.get('macd_histogram', 0)
    
    # Strong disagreement: price above VWAP but momentum and MACD bearish
    if vwap_dev > 0.003 and momentum < -0.1 and macd_hist < 0 and stoch_k < 45:
        return "skip"
    
    # Strong disagreement: price below VWAP but momentum and MACD bullish
    if vwap_dev < -0.003 and momentum > 0.1 and macd_hist > 0 and stoch_k > 55:
        return "skip"
    
    return prediction