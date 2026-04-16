def guard(features: dict, prediction: str) -> str:
    """Filter signals when both Bollinger position and Stochastic show extreme conditions."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if both indicators show overbought (reversal risk)
    if bb_pct_b > 0.9 and stoch_k > 80:
        return "skip"
    
    # Skip if both indicators show oversold (reversal risk)
    if bb_pct_b < 0.1 and stoch_k < 20:
        return "skip"
    
    return prediction