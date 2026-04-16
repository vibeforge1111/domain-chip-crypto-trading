def guard(features: dict, prediction: str) -> str:
    """Skip trades when momentum is decelerating (macd_histogram near zero)."""
    macd = features.get('macd_histogram', 0)
    vol = features.get('volume_ratio', 1)
    
    # Momentum weakening: histogram near zero with low volume
    if abs(macd) < 0.0002 and vol < 0.6:
        return 'skip'
    
    return prediction