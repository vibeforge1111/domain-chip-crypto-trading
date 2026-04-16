def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum score disagree."""
    # Skip if price too far from VWAP (uncertainty)
    if abs(features['vwap_deviation']) > 0.015:
        return "skip"
    
    # Skip if momentum contradicts VWAP position
    if features['momentum_score'] > 0.2 and features['vwap_deviation'] < -0.003:
        return "skip"
    if features['momentum_score'] < -0.2 and features['vwap_deviation'] > 0.003:
        return "skip"
    
    # Skip if stochastic disagrees with momentum direction
    if features['stoch_k'] < 25 and features['momentum_score'] > 0.15:
        return "skip"
    if features['stoch_k'] > 75 and features['momentum_score'] < -0.15:
        return "skip"
    
    return prediction