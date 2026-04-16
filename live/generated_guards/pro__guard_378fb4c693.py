def guard(features: dict, prediction: str) -> str:
    """Filter trades when price is at Bollinger Band and Stochastic extremes."""
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Skip long when overbought: BB near upper band AND Stochastic overbought
    if prediction == 'long' and bb > 0.85 and stoch > 80:
        return 'skip'
    
    # Skip short when oversold: BB near lower band AND Stochastic oversold
    if prediction == 'short' and bb < 0.15 and stoch < 20:
        return 'skip'
    
    return prediction