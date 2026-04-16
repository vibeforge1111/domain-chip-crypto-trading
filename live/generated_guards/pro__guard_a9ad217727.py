def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression to filter bad trades."""
    bb_width = features.get("bb_width", 0)
    atr_ratio = features.get("atr_ratio", 1)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    rsi_2h = features.get("rsi_2h", 50)
    
    # True compression: tight BB AND low ATR
    is_compressed = bb_width < 0.05 and atr_ratio < 0.7
    
    if is_compressed:
        # In compression: require stochastic alignment and reasonable VWAP position
        if prediction == "long" and (stoch_k < 20 or stoch_d < 20):
            return prediction  # Oversold bounce likely - valid
        if prediction == "short" and (stoch_k > 80 or stoch_d > 80):
            return prediction  # Overbought dump likely - valid
        
        # False compression signal: stochastic middle with extreme VWAP
        if 30 <= stoch_k <= 70 and abs(vwap_dev) > 0.01:
            return "skip"
    
    # Loose compression (high atr + high bb_width) often produces false signals
    if atr_ratio > 1.3 and bb_width > 0.1:
        return "skip"
    
    return prediction