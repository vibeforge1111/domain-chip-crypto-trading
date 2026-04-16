def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree with direction."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    stoch_k = features.get("stoch_k", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Skip longs when price below VWAP, negative momentum, and near lower BB
    if prediction == "long" and vwap_dev < -0.008 and momentum < -0.1 and bb_pct_b < 0.2:
        return "skip"
    
    # Skip shorts when price above VWAP, positive momentum, and near upper BB
    if prediction == "short" and vwap_dev > 0.008 and momentum > 0.1 and bb_pct_b > 0.8:
        return "skip"
    
    return prediction