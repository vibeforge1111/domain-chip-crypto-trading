def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using BB and Stochastic."""
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if both BB and Stochastic confirm overbought
    if bb_pct > 0.88 and stoch_k > 78:
        return "skip"
    
    # Skip if both BB and Stochastic confirm oversold
    if bb_pct < 0.12 and stoch_k < 22:
        return "skip"
    
    return prediction