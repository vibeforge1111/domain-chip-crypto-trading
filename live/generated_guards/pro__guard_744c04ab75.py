def guard(features: dict, prediction: str) -> str:
    """Filter trades based on momentum-trend alignment and volatility regime."""
    momentum = features.get('momentum_score', 0)
    volatility = features.get('volatility_regime', 0.5)
    trend = features.get('trend_strength', 0)
    bb_pos = features.get('bb_position', 0.5)
    
    # Reject trades where momentum contradicts strong trend
    if trend > 0.7 and momentum < -0.15:
        return "skip"
    if trend < -0.7 and momentum > 0.15:
        return "skip"
    
    # Skip in extreme volatility with weak alignment
    if volatility > 0.85 and abs(momentum) < 0.25:
        return "skip"
    
    # Skip if price at extreme BB position in high volatility
    if volatility > 0.7 and (bb_pos > 0.9 or bb_pos < 0.1):
        return "skip"
    
    return prediction