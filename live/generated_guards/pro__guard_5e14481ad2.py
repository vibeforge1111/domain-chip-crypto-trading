def guard(features: dict, prediction: str) -> str:
    """Reject trades during false compression setups."""
    # True compression requires BOTH low ATR and low BB width
    atr_compressed = features.get('atr_ratio', 1.0) < 0.7
    bb_compressed = features.get('bb_width', 1.0) < 0.5
    
    # False compression: mixed signals from volatility indicators
    if atr_compressed != bb_compressed:
        return "skip"
    
    # Price sitting at VWAP during compression = indecision/false squeeze
    vwap_dev = abs(features.get('vwap_deviation', 0))
    if vwap_dev < 0.002:
        return "skip"
    
    # Reject compression trades when 2h RSI shows exhaustion (compression likely false)
    rsi_2h = features.get('rsi_2h', 50)
    if rsi_2h < 30 or rsi_2h > 70:
        return "skip"
    
    # Stochastic extremes during compression suggest false signal
    stoch_k = features.get('stoch_k', 50)
    if stoch_k > 85 or stoch_k < 15:
        return "skip"
    
    return prediction