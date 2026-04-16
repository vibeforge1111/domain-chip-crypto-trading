def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum_score and vwap_deviation disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Long: positive momentum but price below VWAP (disagreement)
    if prediction == "long" and momentum > 0.4 and vwap_dev < -0.003:
        return "skip"
    
    # Short: negative momentum but price above VWAP (disagreement)
    if prediction == "short" and momentum < -0.4 and vwap_dev > 0.003:
        return "skip"
    
    return prediction