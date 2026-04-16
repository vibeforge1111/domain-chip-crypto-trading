def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP/momentum disagreement or weak stochastic confirmation."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Disagreement: price far from VWAP but momentum contradicts direction
    if vwap_dev > 0.008 and momentum < -0.3:
        return "skip"
    if vwap_dev < -0.008 and momentum > 0.3:
        return "skip"
    
    # Stochastic overbought/oversold conflict with prediction
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    # Stochastic divergence (K and D disagree)
    if abs(stoch_k - stoch_d) > 20:
        return "skip"
    
    return prediction