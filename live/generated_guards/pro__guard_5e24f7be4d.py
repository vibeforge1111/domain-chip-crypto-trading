def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP-momentum disagreement or extreme stochastic-momentum divergence."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Price below VWAP but bullish momentum (contradiction)
    if vwap_dev < -0.008 and momentum > 0.35:
        return "skip"
    # Price above VWAP but bearish momentum (contradiction)
    if vwap_dev > 0.008 and momentum < -0.35:
        return "skip"
    # Stochastic overbought with positive momentum (weak long)
    if stoch_k > 85 and momentum > 0.25:
        return "skip"
    # Stochastic oversold with negative momentum (weak short)
    if stoch_k < 15 and momentum < -0.25:
        return "skip"
    
    return prediction