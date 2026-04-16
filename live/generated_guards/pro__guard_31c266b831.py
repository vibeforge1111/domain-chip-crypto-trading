def guard(features: dict, prediction: str) -> str:
    """Filter trades in low momentum + high volatility (choppy market) or weak candles."""
    momentum = features.get('momentum_score', 0.5)
    volatility = features.get('volatility_regime', 0.5)
    body = features.get('body_ratio', 0.5)
    trend_strength = features.get('trend_strength', 0.5)
    
    # Skip if momentum is weak and volatility is high (choppy market)
    if momentum < 0.35 and volatility > 0.65:
        return "skip"
    
    # Skip if candle has tiny body in high volatility (potential whipsaw)
    if body < 0.25 and volatility > 0.7:
        return "skip"
    
    # Skip if trend strength is weak despite having a prediction (no conviction)
    if trend_strength < 0.25 and prediction != "skip":
        return "skip"
    
    return prediction