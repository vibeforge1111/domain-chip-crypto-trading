def guard(features: dict, prediction: str) -> str:
    """Filter trades using extreme Bollinger Band positions with stochastic confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Longs only valid at extreme lower band with oversold stochastic
    if prediction == "long" and (bb_pct_b >= 0.05 or stoch_k >= 30):
        return "skip"
    
    # Shorts only valid at extreme upper band with overbought stochastic
    if prediction == "short" and (bb_pct_b <= 0.95 or stoch_k <= 70):
        return "skip"
    
    return prediction