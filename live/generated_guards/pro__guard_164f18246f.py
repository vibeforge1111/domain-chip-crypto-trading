def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like vwap_deviation, momentum_score, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Filter when momentum and VWAP position disagree
    if prediction == 'long':
        # Long wants positive momentum and price above VWAP
        if momentum > 0 and vwap_dev < -0.003:
            return "skip"
    elif prediction == 'short':
        # Short wants negative momentum and price below VWAP
        if momentum < 0 and vwap_dev > 0.003:
            return "skip"
    
    return prediction