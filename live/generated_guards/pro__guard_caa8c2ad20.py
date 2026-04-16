def guard(features: dict, prediction: str) -> str:
    """Filter trades based on RSI extremes amplified by high volatility."""
    rsi = features.get('rsi_14', 50)
    vol_regime = features.get('volatility_regime', 0.5)
    
    # Skip overbought/oversold signals when volatility is elevated
    if vol_regime > 1.3 and (rsi < 35 or rsi > 65):
        return "skip"
    
    return prediction