def guard(features: dict, prediction: str) -> str:
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip longs when wider timeframe is oversold (weak trend context)
    if prediction == 'long' and rsi_2h < 35:
        return 'skip'
    
    # Skip shorts when wider timeframe is overbought (weak trend context)
    if prediction == 'short' and rsi_2h > 65:
        return 'skip'
    
    return prediction