def guard(features: dict, prediction: str) -> str:
    """Filter trades based on MACD momentum deceleration."""
    macd_hist = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == 'long':
        # Reject if momentum is decelerating (near-zero histogram) with overbought 2h RSI
        if abs(macd_hist) < 0.00015 and rsi_2h > 65:
            return 'skip'
        # Reject if momentum weakening with overbought stochastic
        if macd_hist < 0 and stoch_k > 80:
            return 'skip'
    
    if prediction == 'short':
        # Reject if momentum is decelerating (near-zero histogram) with oversold 2h RSI
        if abs(macd_hist) < 0.00015 and rsi_2h < 35:
            return 'skip'
        # Reject if momentum weakening with oversold stochastic
        if macd_hist > 0 and stoch_k < 20:
            return 'skip'
    
    return prediction