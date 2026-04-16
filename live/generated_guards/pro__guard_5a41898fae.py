def guard(features: dict, prediction: str) -> str:
    """Filter trades when Bollinger position and Stochastic confirm extreme conditions."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs when both indicators show overbought extremes
    if prediction == 'long' and bb_pct_b > 0.85 and stoch_k > 80:
        return 'skip'
    
    # Skip shorts when both indicators show oversold extremes
    if prediction == 'short' and bb_pct_b < 0.15 and stoch_k < 20:
        return 'skip'
    
    return prediction