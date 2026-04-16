def guard(features: dict, prediction: str) -> str:
    """Skip trades when both Bollinger Band position and Stochastic reach extreme overbought/oversold levels."""
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Both overbought - reject long signals
    if bb > 0.90 and stoch > 80:
        return "skip"
    # Both oversold - reject short signals  
    if bb < 0.10 and stoch < 20:
        return "skip"
    
    return prediction