def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Overbought: both Bollinger position and stochastic in upper extreme
    overbought = bb_pct_b > 0.82 and stoch_k > 75 and stoch_d > 75
    # Oversold: both Bollinger position and stochastic in lower extreme
    oversold = bb_pct_b < 0.18 and stoch_k < 25 and stoch_d < 25
    
    # Confirm with wider timeframe RSI for strength
    if prediction == 'long' and overbought and rsi_2h > 60:
        return 'skip'
    if prediction == 'short' and oversold and rsi_2h < 40:
        return 'skip'
    
    return prediction