def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP deviation and momentum score disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Disagreement: momentum and VWAP position contradict each other
    if momentum * vwap_dev < -0.01:
        # Momentum and price position point in opposite directions
        if prediction == 'long' and momentum < 0:
            return 'skip'
        if prediction == 'short' and momentum > 0:
            return 'skip'
    
    return prediction