def guard(features: dict, prediction: str) -> str:
    """Volatility-adjusted momentum filter - skip stretched RSI in high volatility with weak trend."""
    rsi = features.get('rsi_14', 50)
    vol_regime = features.get('volatility_regime', 0.5)
    trend = features.get('trend_strength', 0.5)
    bb_width = features.get('bb_width', 0.02)
    
    # Skip stretched RSI during high volatility unless strong trend and wide bands
    if vol_regime > 0.6:
        if (rsi > 70 or rsi < 30) and trend < 0.45 and bb_width < 0.03:
            return "skip"
    
    return prediction