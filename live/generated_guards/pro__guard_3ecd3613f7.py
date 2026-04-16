def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes and Stochastic confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    volume_ratio = features.get('volume_ratio', 1.0)
    
    if prediction == 'long':
        # Long only at lower band extremes with oversold confirmation
        if not (bb_pct_b < 0.10 and stoch_k < 25):
            return 'skip'
    elif prediction == 'short':
        # Short only at upper band extremes with overbought confirmation
        if not (bb_pct_b > 0.90 and stoch_k > 75):
            return 'skip'
    
    # Require above-average volume for conviction
    if volume_ratio < 1.0:
        return 'skip'
    
    return prediction