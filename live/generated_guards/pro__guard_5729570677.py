def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes as high-confidence entry zones."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Long only at extreme oversold (bb_pct_b < 0.05) with stoch confirmation
    if prediction == "long" and bb_pct_b < 0.05 and stoch_k > 20:
        return prediction
    
    # Short only at extreme overbought (bb_pct_b > 0.95) with stoch confirmation
    if prediction == "short" and bb_pct_b > 0.95 and stoch_k < 80:
        return prediction
    
    return "skip"