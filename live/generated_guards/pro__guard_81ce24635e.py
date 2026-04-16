def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard with multi-timeframe confirmation."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    diff = stoch_k - stoch_d
    
    # Filter weak crossovers (tight spread = unreliable signal)
    if abs(diff) < 5 or abs(diff) > 25:
        return "skip"
    
    if prediction == "long":
        # Bullish crossover: k crosses above d
        if diff > 0 and vwap_dev > 0 and rsi_2h > 50 and bb_pct_b > 0.25:
            return prediction
    
    elif prediction == "short":
        # Bearish crossover: k crosses below d
        if diff < 0 and vwap_dev < 0 and rsi_2h < 50 and bb_pct_b < 0.75:
            return prediction
    
    return "skip"