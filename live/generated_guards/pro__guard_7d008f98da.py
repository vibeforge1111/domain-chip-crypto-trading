def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes with confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Long: extreme lower band + oversold stochastic + 2h not overbought
    if prediction == 'long' and bb_pct_b < 0.05 and stoch_k < 20 and rsi_2h < 70:
        return prediction
    
    # Short: extreme upper band + overbought stochastic + 2h not oversold
    if prediction == 'short' and bb_pct_b > 0.95 and stoch_k > 80 and rsi_2h > 30:
        return prediction
    
    return 'skip'