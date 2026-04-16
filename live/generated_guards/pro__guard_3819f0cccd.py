def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP/momentum disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    mom_score = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Price above VWAP but momentum bearish and stoch overbought
    if vwap_dev > 0.008 and mom_score < -0.1 and stoch_k > 70:
        return "skip"
    
    # Price below VWAP but momentum bullish and stoch oversold
    if vwap_dev < -0.008 and mom_score > 0.1 and stoch_k < 30:
        return "skip"
    
    # Skip if 2h RSI disagrees with prediction direction
    if prediction == "long" and rsi_2h < 35:
        return "skip"
    if prediction == "short" and rsi_2h > 65:
        return "skip"
    
    return prediction