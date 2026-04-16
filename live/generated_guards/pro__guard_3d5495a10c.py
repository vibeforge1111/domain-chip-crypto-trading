def guard(features: dict, prediction: str) -> str:
    """Filter trades when both Bollinger Band position and Stochastic indicate extreme conditions."""
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Long signals: skip if both BB and Stochastic show overbought (extreme)
    if prediction == 'long' and bb > 0.88 and stoch > 78:
        return 'skip'
    
    # Short signals: skip if both BB and Stochastic show oversold (extreme)
    if prediction == 'short' and bb < 0.12 and stoch < 22:
        return 'skip'
    
    return prediction