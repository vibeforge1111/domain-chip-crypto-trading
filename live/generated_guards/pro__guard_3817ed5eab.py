def guard(features: dict, prediction: str) -> str:
    """Filter signals during compression with momentum confirmation."""
    if prediction == "skip":
        return prediction
    
    bb_width = features.get("bb_width", 1.0)
    atr_ratio = features.get("atr_ratio", 1.0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    
    # Detect compression: low bb_width and low atr_ratio
    is_compressed = bb_width < 0.5 and atr_ratio < 0.7
    
    if is_compressed:
        # False compression: extreme oscillators without momentum
        stoch_extreme = (stoch_k > 80 and stoch_d > 80) or (stoch_k < 20 and stoch_d < 20)
        no_momentum = obv_slope <= 0 and macd_histogram <= 0
        
        if stoch_extreme and no_momentum:
            return "skip"
    
    return prediction