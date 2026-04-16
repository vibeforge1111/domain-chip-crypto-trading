def guard(features: dict, prediction: str) -> str:
    """Filter trades with poor candle structure, weak momentum, or low volatility."""
    # Require minimum body ratio for reliable candle structure
    if features['body_ratio'] < 0.25:
        return "skip"
    
    # Skip if momentum is weak regardless of direction
    if abs(features['momentum_score']) < 0.35:
        return "skip"
    
    # Skip if BBands are in squeeze (potential false breakout)
    if features['bb_width'] < 0.02:
        return "skip"
    
    return prediction