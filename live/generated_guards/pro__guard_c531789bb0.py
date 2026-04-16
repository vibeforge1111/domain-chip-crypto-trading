def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum score disagree."""
    vwap_deviation = features.get('vwap_deviation', 0)
    momentum_score = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Filter long if below VWAP but momentum is bearish
    if prediction == 'long' and momentum_score < -0.25 and vwap_deviation < -0.005:
        return "skip"
    
    # Filter short if above VWAP but momentum is bullish
    if prediction == 'short' and momentum_score > 0.25 and vwap_deviation > 0.005:
        return "skip"
    
    # Filter if stochastic confirms disagreement (overbought for long, oversold for short)
    if prediction == 'long' and stoch_k > 80 and stoch_d > 75:
        return "skip"
    if prediction == 'short' and stoch_k < 20 and stoch_d < 25:
        return "skip"
    
    return prediction