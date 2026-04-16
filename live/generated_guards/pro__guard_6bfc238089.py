def guard(features: dict, prediction: str) -> str:
    """Reject signals in volatile chop with weak momentum."""
    if prediction == "skip":
        return prediction
    
    vol_spike = features.get('atr_ratio', 1.0) > 1.4
    weak_body = features.get('body_ratio', 0.5) < 0.35
    no_trend = abs(features.get('ema_slope', 0)) < 0.001
    high_vol = features.get('volume_ratio', 1.0) > 1.5
    
    if vol_spike and weak_body and (no_trend or high_vol):
        return "skip"
    
    return prediction