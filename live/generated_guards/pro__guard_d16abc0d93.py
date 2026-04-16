def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with market features
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Skip if price too close to VWAP (within 0.3% either side)
    if abs(vwap_dev) < 0.003:
        # Confirm with weak stochastic alignment
        if (prediction == "long" and stoch_k < 30) or (prediction == "short" and stoch_k > 70):
            return "skip"
    
    return prediction