def guard(features: dict, prediction: str) -> str:
    """Filter trades where wick structure contradicts trend momentum (exhaustion pattern)."""
    upper_wick = features.get('upper_wick_ratio', 0)
    lower_wick = features.get('lower_wick_ratio', 0)
    trend_strength = features.get('trend_strength', 0)
    volume_ratio = features.get('volume_ratio', 1)
    bb_position = features.get('bb_position', 0.5)
    
    # Wick exhaustion: large wick against trend in BB extremities with volume confirmation
    long_exhaustion = (prediction == 'long' and 
                       upper_wick > 0.35 and 
                       trend_strength > 0.2 and 
                       bb_position > 0.85 and 
                       volume_ratio > 1.3)
    
    short_exhaustion = (prediction == 'short' and 
                        lower_wick > 0.35 and 
                        trend_strength > 0.2 and 
                        bb_position < 0.15 and 
                        volume_ratio > 1.3)
    
    if long_exhaustion or short_exhaustion:
        return "skip"
    
    return prediction