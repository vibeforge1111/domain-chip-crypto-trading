def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes with momentum and volume confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    volume_ratio = features.get("volume_ratio", 1.0)
    
    # Long setup: price near lower band with oversold momentum and volume surge
    if bb_pct_b < 0.05 and prediction == "long" and stoch_k < 30 and volume_ratio > 1.0:
        return prediction
    
    # Short setup: price near upper band with overbought momentum and volume surge
    if bb_pct_b > 0.95 and prediction == "short" and stoch_k > 70 and volume_ratio > 1.0:
        return prediction
    
    return "skip"