def guard(features: dict, prediction: str) -> str:
    """Oscillator Momentum Confirmation Filter - rejects trades without momentum alignment."""
    rsi = features.get('rsi_14', 50)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Check for oscillator divergence (momentum disagreement)
    # Overbought divergence: RSI elevated but stochastic not confirming
    if rsi > 70 and stoch_k < 70 and stoch_d < 70:
        return "skip"
    # Oversold divergence: RSI depressed but stochastic not confirming  
    if rsi < 30 and stoch_k > 30 and stoch_d > 30:
        return "skip"
    
    return prediction