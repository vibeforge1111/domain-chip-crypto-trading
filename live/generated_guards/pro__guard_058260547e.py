def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum score disagree with prediction."""
    vwap_deviation = features.get('vwap_deviation', 0)
    momentum_score = features.get('momentum_score', 0)
    
    if prediction == 'long':
        # Skip if both momentum and VWAP signal weakness
        if momentum_score < -0.2 and vwap_deviation < -0.015:
            return 'skip'
    elif prediction == 'short':
        # Skip if both momentum and VWAP signal strength
        if momentum_score > 0.2 and vwap_deviation > 0.015:
            return 'skip'
    
    return prediction