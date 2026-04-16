def guard(features: dict, prediction: str) -> str:
    """Filter false compression breakouts using ATR, BB, and momentum divergence."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.5)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    macd_histogram = features.get('macd_histogram', 0.0)
    obv_slope = features.get('obv_slope', 0.0)
    
    # True compression: low ATR + narrow bands
    is_compression = atr_ratio < 0.65 and bb_width < 0.35
    
    # At extreme of Bollinger Bands
    at_extreme = bb_pct_b < 0.2 or bb_pct_b > 0.8
    
    # Momentum divergence from direction of trade
    momentum_against = (prediction == "long" and macd_histogram < -0.0001) or (prediction == "short" and macd_histogram > 0.0001)
    
    # OBV not confirming direction
    volume_not_confirming = (prediction == "long" and obv_slope < 0) or (prediction == "short" and obv_slope > 0)
    
    # False compression trap: tight + extreme + weak momentum/volume
    if is_compression and at_extreme and (momentum_against or volume_not_confirming):
        return "skip"
    
    return prediction