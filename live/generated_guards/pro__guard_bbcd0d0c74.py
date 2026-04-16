def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band position and Stochastic extremes."""
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Skip longs when overbought on both indicators
    if prediction == 'long' and bb > 0.85 and stoch > 80:
        return 'skip'
    
    # Skip shorts when oversold on both indicators
    if prediction == 'short' and bb < 0.15 and stoch < 20:
        return 'skip'
    
    return prediction