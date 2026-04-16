def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard with multi-timeframe confirmation."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    macd_histogram = features.get('macd_histogram', 0)
    
    stoch_diff = stoch_k - stoch_d
    
    if prediction == "long":
        if stoch_diff <= 0:
            return "skip"
        if stoch_diff > 20:
            return "skip"
        if rsi_2h < 45:
            return "skip"
        if bb_pct_b > 0.75:
            return "skip"
        if macd_histogram < 0:
            return "skip"
    
    elif prediction == "short":
        if stoch_diff >= 0:
            return "skip"
        if stoch_diff < -20:
            return "skip"
        if rsi_2h > 55:
            return "skip"
        if bb_pct_b < 0.25:
            return "skip"
        if macd_histogram > 0:
            return "skip"
    
    return prediction