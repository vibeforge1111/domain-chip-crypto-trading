def guard(features: dict, prediction: str) -> str:
    """Skip trades where vwap_deviation and momentum_score disagree."""
    vwap_deviation = features.get('vwap_deviation', 0)
    momentum_score = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    if prediction == "long":
        # Reject if price far above VWAP but momentum weak and stochastic overbought
        if vwap_deviation > 0.015 and momentum_score < 0 and stoch_k > 75:
            return "skip"
    elif prediction == "short":
        # Reject if price far below VWAP but momentum strong and stochastic oversold
        if vwap_deviation < -0.015 and momentum_score > 0 and stoch_k < 25:
            return "skip"
    
    return prediction