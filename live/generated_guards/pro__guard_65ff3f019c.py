def guard(features: dict, prediction: str) -> str:
    """Filter trades during low-volatility compression phases.
    
    Reject signals when Bollinger Bands are squeezed (low width) AND
    candle body is small relative to range - indicating indecision
    before a potential false breakout.
    """
    bb_squeezed = features.get('bb_width', 1.0) < 0.015
    small_body = features.get('body_ratio', 1.0) < 0.3
    low_volume = features.get('volume_ratio', 1.0) < 0.7
    
    if bb_squeezed and small_body and low_volume:
        return "skip"
    
    return prediction