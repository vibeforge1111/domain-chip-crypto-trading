def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP and momentum disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Long: reject if above VWAP but momentum bearish AND stoch overbought
    if prediction == "long" and vwap_dev > 0.008 and momentum < -0.2 and stoch_k > 70:
        return "skip"
    
    # Short: reject if below VWAP but momentum bullish AND stoch oversold
    if prediction == "short" and vwap_dev < -0.008 and momentum > 0.2 and stoch_k < 30:
        return "skip"
    
    return prediction