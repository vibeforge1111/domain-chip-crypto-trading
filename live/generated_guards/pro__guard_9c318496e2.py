def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    vwap_dev = features.get('vwap_deviation', 0)
    mom_score = features.get('momentum_score', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if vwap and momentum strongly disagree
    if vwap_dev > 0.008 and mom_score < 0.35 and stoch_k < 40:
        return "skip"
    if vwap_dev < -0.008 and mom_score > 0.65 and stoch_k > 60:
        return "skip"
    
    return prediction