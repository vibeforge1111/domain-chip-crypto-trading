def guard(features: dict, prediction: str) -> str:
    """Filter trades when RSI is extreme and market conditions are unfavorable."""
    rsi = features.get('rsi_14', 50)
    volatility = features.get('volatility_regime', 0.5)
    trend_strength = features.get('trend_strength', 0)
    
    # Skip if overbought/oversold AND (weak trend OR high volatility)
    if (rsi > 70 or rsi < 30) and (trend_strength < 0.3 or volatility > 0.7):
        return "skip"
    
    return prediction