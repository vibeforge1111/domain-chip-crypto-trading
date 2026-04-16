def guard(features: dict, prediction: str) -> str:
    """Skip trades misaligned with broader trend (rsi_2h)."""
    rsi_2h = features.get('rsi_2h', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long' and rsi_2h > 70:
        return 'skip'
    if prediction == 'short' and rsi_2h < 30:
        return 'skip'
    
    if prediction == 'long' and rsi_2h < 40 and stoch_d < 20:
        return 'skip'
    if prediction == 'short' and rsi_2h > 60 and stoch_d > 80:
        return 'skip'
    
    return prediction