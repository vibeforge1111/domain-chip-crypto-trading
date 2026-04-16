def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover timing and momentum confirmation."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Calculate stochastic alignment (positive = bullish, negative = bearish)
    sto_diff = stoch_k - stoch_d
    
    # For LONG entries: require bullish stochastic crossover + not overbought
    if prediction == "long":
        if sto_diff <= 0:
            return "skip"  # No bullish crossover
        if stoch_k > 80:
            return "skip"  # Already overbought, likely reversal risk
    
    # For SHORT entries: require bearish stochastic crossover + not oversold
    if prediction == "short":
        if sto_diff >= 0:
            return "skip"  # No bearish crossover
        if stoch_k < 20:
            return "skip"  # Already oversold, likely reversal risk
    
    # Additional context: avoid counter-trend trades in wider timeframe
    if prediction == "long" and rsi_2h > 70:
        return "skip"  # Wider timeframe overbought, headwind
    if prediction == "short" and rsi_2h < 30:
        return "skip"  # Wider timeframe oversold, headwind
    
    return prediction