def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extremes for entry filtering."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    obv_slope = features.get('obv_slope', 0)
    
    # High-confidence entry zones: BB extremes
    # Lower band extreme (<0.05): valid for long entries
    if bb_pct_b < 0.05:
        if prediction == "long" and stoch_k < 25 and obv_slope > 0:
            return prediction
        return "skip"
    
    # Upper band extreme (>0.95): valid for short entries
    if bb_pct_b > 0.95:
        if prediction == "short" and stoch_k > 75 and obv_slope < 0:
            return prediction
        return "skip"
    
    return "skip"