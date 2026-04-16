def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band position and Stochastic extremes."""
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Reject longs at extreme overbought (upper BB + stoch > 80)
    if prediction == 'long' and bb_pct > 0.85 and stoch_k > 80:
        return 'skip'
    
    # Reject shorts at extreme oversold (lower BB + stoch < 20)
    if prediction == 'short' and bb_pct < 0.15 and stoch_k < 20:
        return 'skip'
    
    return prediction