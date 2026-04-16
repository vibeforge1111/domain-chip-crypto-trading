def guard(features: dict, prediction: str) -> str:
    """Filter trades not at BB extreme zones for high-confidence entries."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Long only at lower BB extreme with oversold stochastic
    if prediction == "long" and (bb_pct_b >= 0.05 or stoch_k >= 20):
        return "skip"
    
    # Short only at upper BB extreme with overbought stochastic
    if prediction == "short" and (bb_pct_b <= 0.95 or stoch_k <= 80):
        return "skip"
    
    return prediction