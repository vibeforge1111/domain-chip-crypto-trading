def guard(features: dict, prediction: str) -> str:
    """Filter false compression breakouts using volatility and momentum divergence."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    stoch_k = features.get('stoch_k', 50)
    obv_slope = features.get('obv_slope', 0)
    macd_histogram = features.get('macd_histogram', 0)
    
    # True compression: both BB width and ATR ratio are low
    is_compression = bb_width < 0.75 and atr_ratio < 0.8
    
    if is_compression and prediction != "skip":
        # False compression: price at BB extremes during compression
        at_band_extreme = bb_pct_b < 0.15 or bb_pct_b > 0.85
        # False compression: RSI extreme in wider timeframe
        rsi_extreme = rsi_2h < 25 or rsi_2h > 75
        # False compression: momentum divergence (price compressed but momentum deteriorating)
        momentum_divergence = macd_histogram < -0.001 and obv_slope < 0
        
        if at_band_extreme or rsi_extreme or momentum_divergence:
            return "skip"
    
    return prediction