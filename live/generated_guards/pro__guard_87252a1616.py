def guard(features: dict, prediction: str) -> str:
    """Filter trades that contradict the broader 2-hour trend."""
    rsi_2h = features.get('rsi_2h', 50)
    momentum = features.get('momentum_score', 0)
    
    # Long trades rejected if broader timeframe shows weakness
    if prediction == "long" and rsi_2h < 45 and momentum < 0:
        return "skip"
    
    # Short trades rejected if broader timeframe shows strength
    if prediction == "short" and rsi_2h > 55 and momentum > 0:
        return "skip"
    
    return prediction