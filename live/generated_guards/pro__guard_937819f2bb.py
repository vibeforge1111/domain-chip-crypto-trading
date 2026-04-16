def guard(features: dict, prediction: str) -> str:
    """Custom guard using Bollinger Band extreme zones for entry confirmation."""
    bb = features.get('bb_pct_b', 0.5)
    vol = features.get('volume_ratio', 1.0)
    rsi = features.get('rsi_14', 50)
    
    if prediction == 'long':
        if bb >= 0.10 or rsi >= 40:
            return 'skip'
    elif prediction == 'short':
        if bb <= 0.90 or rsi <= 60:
            return 'skip'
    
    return prediction