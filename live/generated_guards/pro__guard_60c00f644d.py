def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree with prediction."""
    vwap = features.get("vwap_deviation", 0)
    mom = features.get("momentum_score", 0)
    
    # For longs: skip if both momentum bearish AND price below VWAP
    if prediction == "long" and mom < -5 and vwap < -0.002:
        return "skip"
    
    # For shorts: skip if both momentum bullish AND price above VWAP
    if prediction == "short" and mom > 5 and vwap > 0.002:
        return "skip"
    
    return prediction