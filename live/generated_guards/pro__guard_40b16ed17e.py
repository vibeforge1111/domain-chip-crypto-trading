def guard(features: dict, prediction: str) -> str:
    """Filter trades when wick imbalance contradicts direction in trending conditions."""
    upper_wick = features.get('upper_wick_ratio', 0)
    lower_wick = features.get('lower_wick_ratio', 0)
    trend_strength = features.get('trend_strength', 0.5)
    
    if trend_strength > 0.6:
        if prediction == 'long' and upper_wick > 0.4:
            return 'skip'
        if prediction == 'short' and lower_wick > 0.4:
            return 'skip'
    
    return prediction