def guard(features: dict, prediction: str) -> str:
    """Filter trades by detecting true vs false compression breakouts."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_14 = features.get('rsi_14', 50.0)
    rsi_2h = features.get('rsi_2h', 50.0)
    stoch_k = features.get('stoch_k', 50.0)
    obv_slope = features.get('obv_slope', 0.0)
    
    # True compression: both ATR and BB width low
    is_compression = atr_ratio < 0.75 and bb_width < 0.15
    
    if not is_compression:
        return prediction
    
    # False compression signals often have extreme RSI in wider timeframe
    if rsi_2h > 75 and prediction == "short":
        return "skip"
    if rsi_2h < 25 and prediction == "long":
        return "skip"
    
    # Stochastic divergence in compression signals weak setups
    if stoch_k > 80 and prediction == "long":
        return "skip"
    if stoch_k < 20 and prediction == "short":
        return "skip"
    
    # Volume/momentum confirmation required in compression
    if obv_slope <= 0 and prediction == "long":
        return "skip"
    if obv_slope >= 0 and prediction == "short":
        return "skip"
    
    return prediction