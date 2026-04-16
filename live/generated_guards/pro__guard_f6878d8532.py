def guard(features: dict, prediction: str) -> str:
    """Filter trades based on momentum-trend alignment and volatility regime."""
    # Skip if volatility regime is too extreme
    if features['volatility_regime'] > 0.85 or features['volatility_regime'] < 0.15:
        return "skip"
    
    # Skip if momentum contradicts the trade direction
    if prediction == "long" and features['momentum_score'] < -0.15:
        return "skip"
    if prediction == "short" and features['momentum_score'] > 0.15:
        return "skip"
    
    # Skip if trend strength is weak AND momentum is neutral
    if abs(features['trend_strength']) < 0.3 and abs(features['momentum_score']) < 0.2:
        return "skip"
    
    return prediction