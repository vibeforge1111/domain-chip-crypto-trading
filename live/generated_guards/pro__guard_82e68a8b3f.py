def guard(features: dict, prediction: str) -> str:
    """Skip false breakouts from compression without momentum support."""
    is_compression = features['atr_ratio'] < 0.75 and features['bb_width'] < 0.6
    inside_bands = 0.25 < features['bb_pct_b'] < 0.75
    lacks_momentum = features['macd_histogram'] <= 0 and features['obv_slope'] <= 0
    weak_context = features['rsi_2h'] < 45
    if is_compression and inside_bands and (lacks_momentum or weak_context):
        return "skip"
    return prediction