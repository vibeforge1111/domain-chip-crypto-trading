def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Stochastic alignment: k above d for longs, k below d for shorts
    stoch_bullish = stoch_k > stoch_d
    stoch_bearish = stoch_k < stoch_d
    
    # Wider timeframe confirmation
    rsi_2h_confirm = (rsi_2h < 50 and prediction == "long") or (rsi_2h > 50 and prediction == "short")
    
    # Reject if prediction contradicts stochastic alignment
    if prediction == "long" and not stoch_bullish:
        return "skip"
    if prediction == "short" and not stoch_bearish:
        return "skip"
    
    # Reject if wider timeframe disagrees
    if not rsi_2h_confirm:
        return "skip"
    
    return prediction