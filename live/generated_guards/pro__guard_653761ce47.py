def guard(features: dict, prediction: str) -> str:
    """Detect false compression: low volatility with weak volume/momentum divergence."""
    # True compression: low atr_ratio and narrow bb_width
    is_compressed = features.get('atr_ratio', 1) > 0.8 or features.get('bb_width', 1) > 0.5
    if is_compressed:
        return prediction
    
    # False compression signals: weak OBV slope (no accumulation) + overbought stoch
    weak_volume = features.get('obv_slope', 0) < 0
    stoch_overbought = features.get('stoch_k', 50) > 80
    
    # Also check RSI divergence between timeframes
    rsi_divergence = features.get('rsi_2h', 50) - features.get('rsi_14', 50) > 10
    
    if weak_volume and (stoch_overbought or rsi_divergence):
        return "skip"
    
    return prediction