def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover and momentum alignment."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    obv_slope = features.get('obv_slope', 0)
    rsi_2h = features.get('rsi_2h', 50)

    if prediction == 'long':
        # Reject if stoch_k already crossed above (late entry) or no oversold alignment
        if stoch_k > stoch_d or stoch_k > 30:
            return "skip"
        # Reject if momentum diverges
        if obv_slope <= 0 or rsi_2h < 45:
            return "skip"
    elif prediction == 'short':
        # Reject if stoch_k already crossed below (late entry) or no overbought alignment
        if stoch_k < stoch_d or stoch_k < 70:
            return "skip"
        # Reject if momentum diverges
        if obv_slope >= 0 or rsi_2h > 55:
            return "skip"

    return prediction