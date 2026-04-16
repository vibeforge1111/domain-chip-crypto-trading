def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # For long entries, require bullish stochastic alignment
    # stoch_k must be above stoch_d (bullish crossover occurred or occurring)
    if prediction == 'long':
        if stoch_k <= stoch_d:
            return "skip"
        # Reject if both oscillators are in overbought territory (overextended)
        if stoch_k > 70 and stoch_d > 70:
            return "skip"
    
    # For short entries, require bearish stochastic alignment
    # stoch_k must be below stoch_d (bearish crossover occurred or occurring)
    if prediction == 'short':
        if stoch_k >= stoch_d:
            return "skip"
        # Reject if both oscillators are in oversold territory (oversold bounce likely)
        if stoch_k < 30 and stoch_d < 30:
            return "skip"
    
    return prediction