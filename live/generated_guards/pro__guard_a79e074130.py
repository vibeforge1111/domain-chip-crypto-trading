def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band and Stochastic extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip long when overbought (both BB at upper band + stochastic >80)
    if prediction == 'long' and bb_pct_b > 0.85 and stoch_k > 80:
        return 'skip'
    
    # Skip short when oversold (both BB at lower band + stochastic <20)
    if prediction == 'short' and bb_pct_b < 0.15 and stoch_k < 20:
        return 'skip'
    
    return prediction