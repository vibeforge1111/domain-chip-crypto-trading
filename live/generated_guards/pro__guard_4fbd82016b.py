def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP/momentum disagreement or conflicting stochastic signals."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # VWAP vs momentum disagreement (price below VWAP but bullish momentum)
    if vwap_dev < -0.005 and momentum > 0.3:
        return "skip"
    if vwap_dev > 0.005 and momentum < -0.3:
        return "skip"
    
    # Stochastic divergence filter (stoch K/D disagreeing)
    if abs(stoch_k - stoch_d) > 20:
        return "skip"
    
    # 2h context conflicting with short-term momentum
    if rsi_2h < 40 and momentum > 0.4:
        return "skip"
    if rsi_2h > 60 and momentum < -0.4:
        return "skip"
    
    return prediction