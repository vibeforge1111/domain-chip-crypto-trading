def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme zones with stochastic confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Long entries require extreme lower band + oversold stochastic
    if prediction == 'long':
        if bb_pct_b >= 0.05 or stoch_k >= 30:
            return 'skip'
    
    # Short entries require extreme upper band + overbought stochastic
    if prediction == 'short':
        if bb_pct_b <= 0.95 or stoch_k <= 70:
            return 'skip'
    
    return prediction