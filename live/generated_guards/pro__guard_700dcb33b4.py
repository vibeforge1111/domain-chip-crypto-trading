def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == "long":
        # Accept early bullish crossover: stoch_k rising through stoch_d from oversold
        if stoch_k > 50 or stoch_k >= stoch_d or rsi_2h > 60:
            return "skip"
    
    elif prediction == "short":
        # Accept early bearish crossover: stoch_k falling through stoch_d from overbought
        if stoch_k < 50 or stoch_k <= stoch_d or rsi_2h < 40:
            return "skip"
    
    return prediction