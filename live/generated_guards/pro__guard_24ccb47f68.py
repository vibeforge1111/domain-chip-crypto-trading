def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum indicators disagree with VWAP deviation."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum_score = features.get("momentum_score", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip longs when price is below VWAP (negative deviation) AND momentum is bearish
    if prediction == "long" and vwap_dev < -0.005 and momentum_score < -0.1 and stoch_k < 40:
        return "skip"
    
    # Skip shorts when price is above VWAP (positive deviation) AND momentum is bullish
    if prediction == "short" and vwap_dev > 0.005 and momentum_score > 0.1 and stoch_k > 60:
        return "skip"
    
    return prediction