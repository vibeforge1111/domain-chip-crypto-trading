def guard(features: dict, prediction: str) -> str:
    """Filter trades when Bollinger Bands and Stochastic show extreme overbought/oversold conditions."""
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs when both indicators confirm overbought
    if prediction == 'long' and bb_pct > 0.88 and stoch_k > 82:
        return 'skip'
    
    # Skip shorts when both indicators confirm oversold
    if prediction == 'short' and bb_pct < 0.12 and stoch_k < 18:
        return 'skip'
    
    return prediction