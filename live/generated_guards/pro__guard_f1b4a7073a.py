def guard(features: dict, prediction: str) -> str:
    """Filter trades based on VWAP deviation and momentum disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # VWAP and momentum disagreement
    if vwap_dev > 0.003 and momentum < -0.1:
        return "skip"
    if vwap_dev < -0.003 and momentum > 0.1:
        return "skip"
    
    # Stochastic extremes conflict with momentum
    if stoch_k > 85 and momentum < 0:
        return "skip"
    if stoch_k < 15 and momentum > 0:
        return "skip"
    
    # RSI 2h divergence from short-term overbought/oversold
    if rsi_2h > 65 and stoch_k > 80:
        return "skip"
    if rsi_2h < 35 and stoch_k < 20:
        return "skip"
    
    return prediction