def guard(features: dict, prediction: str) -> str:
    """Guard against momentum-trend divergence and low volatility environments."""
    # Skip if momentum contradicts trend direction
    momentum_score = features.get('momentum_score', 0)
    trend_strength = features.get('trend_strength', 0)
    if momentum_score * trend_strength < 0:
        return "skip"
    
    # Skip if volatility is too low (squeeze or dead market)
    if features.get('volatility_regime', 1) < 0.3:
        return "skip"
    
    # Skip if RSI is in extreme zones (overbought/oversold exhaustion)
    rsi = features.get('rsi_14', 50)
    if rsi > 78 or rsi < 22:
        return "skip"
    
    return prediction