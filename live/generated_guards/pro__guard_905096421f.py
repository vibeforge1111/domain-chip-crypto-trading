def guard(features: dict, prediction: str) -> str:
    """Filter trades using BB extreme zones with stoch momentum confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    if prediction == 'long':
        # Long only valid near lower band with oversold stoch
        if not (bb_pct_b < 0.05 and stoch_k < 25):
            return 'skip'
    
    if prediction == 'short':
        # Short only valid near upper band with overbought stoch
        if not (bb_pct_b > 0.95 and stoch_k > 75):
            return 'skip'
    
    return prediction