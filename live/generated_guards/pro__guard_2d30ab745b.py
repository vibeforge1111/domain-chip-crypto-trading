def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using BB and Stochastic."""
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    vwap = features.get('vwap_deviation', 0)
    
    # Reject longs when overbought: BB near upper band + stochastic overbought
    if prediction == 'long' and bb > 0.90 and stoch > 80:
        return 'skip'
    
    # Reject shorts when oversold: BB near lower band + stochastic oversold
    if prediction == 'short' and bb < 0.10 and stoch < 20:
        return 'skip'
    
    # Additional check: reject longs if price far above VWAP at overbought extremes
    if prediction == 'long' and bb > 0.88 and stoch > 75 and vwap > 0.015:
        return 'skip'
    
    return prediction