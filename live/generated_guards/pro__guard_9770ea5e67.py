def guard(features: dict, prediction: str) -> str:
    """Filter trades using ATR/Bollinger compression detection with RSI divergence."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.02)
    stoch_k = features.get('stoch_k', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    rsi_14 = features.get('rsi_14', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # True compression: low volatility + narrow bands
    is_compressed = atr_ratio < 0.7 and bb_width < 0.015
    
    # Skip if compressed but stochastic is extreme (false signal)
    if is_compressed and (stoch_k > 80 or stoch_k < 20):
        return "skip"
    
    # Skip if compressed but price far from VWAP (unstable)
    if is_compressed and abs(vwap_deviation) > 0.01:
        return "skip"
    
    # Skip on RSI divergence between timeframes
    if rsi_14 > 70 and rsi_2h < 40:
        return "skip"
    if rsi_14 < 30 and rsi_2h > 60:
        return "skip"
    
    return prediction