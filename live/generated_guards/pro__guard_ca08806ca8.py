def guard(features: dict, prediction: str) -> str:
    """Reject signals where VWAP deviation disagrees with momentum and wider RSI."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi_2h = features.get('rsi_2h', 50)
    stoch_k = features.get('stoch_k', 50)
    
    # Price extended above VWAP but momentum/RSI bearish and stoch overbought
    if vwap_dev > 0.015 and momentum < -0.2 and rsi_2h < 45 and stoch_k > 70:
        return "skip"
    
    # Price extended below VWAP but momentum/RSI bullish and stoch oversold
    if vwap_dev < -0.015 and momentum > 0.2 and rsi_2h > 55 and stoch_k < 30:
        return "skip"
    
    return prediction