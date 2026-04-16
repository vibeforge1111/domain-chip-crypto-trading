def guard(features: dict, prediction: str) -> str:
    """Guard using Bollinger Band extremes with stochastic confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    if prediction == 'skip':
        return prediction
    
    # Long: extreme lower band + oversold confirmation
    if prediction == 'long' and bb_pct_b < 0.05 and stoch_k < 25:
        return prediction
    
    # Short: extreme upper band + overbought confirmation
    if prediction == 'short' and bb_pct_b > 0.95 and stoch_k > 75:
        return prediction
    
    return 'skip'