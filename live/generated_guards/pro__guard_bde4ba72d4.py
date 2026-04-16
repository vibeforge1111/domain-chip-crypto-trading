def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Detect crossover: stoch_k crossing above/below stoch_d
    # Using threshold spread to identify crossover conditions
    crossover_gap = stoch_k - stoch_d
    
    if prediction == "long":
        # Long valid when stoch_k crosses above stoch_d in oversold
        if crossover_gap < 5 or stoch_k > 30:
            return "skip"
        # Reject if wider timeframe is overbought
        if rsi_2h > 65:
            return "skip"
            
    elif prediction == "short":
        # Short valid when stoch_k crosses below stoch_d in overbought
        if crossover_gap > -5 or stoch_k < 70:
            return "skip"
        # Reject if wider timeframe is oversold
        if rsi_2h < 35:
            return "skip"
    
    return prediction