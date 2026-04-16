def guard(features: dict, prediction: str) -> str:
    """Filter trades at Bollinger Band and Stochastic extremes."""
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Skip longs when overbought (upper band + high stochastic)
    if prediction == 'long' and bb > 0.9 and stoch > 80:
        return 'skip'
    
    # Skip shorts when oversold (lower band + low stochastic)
    if prediction == 'short' and bb < 0.1 and stoch < 20:
        return 'skip'
    
    return prediction