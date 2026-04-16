def guard(features: dict, prediction: str) -> str:
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip long signals when broader timeframe is overbought (potential reversal)
    if prediction == 'long' and rsi_2h > 75:
        return 'skip'
    
    # Skip short signals when broader timeframe is oversold (potential bounce)
    if prediction == 'short' and rsi_2h < 25:
        return 'skip'
    
    return prediction