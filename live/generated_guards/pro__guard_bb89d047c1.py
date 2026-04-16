def guard(features: dict, prediction: str) -> str:
    """Reject trades when candle structure is unreliable AND momentum contradicts trend."""
    # High wick dominance indicates weak/inconclusive price action
    wick_dominant = features['upper_wick_ratio'] + features['lower_wick_ratio'] > 0.7
    
    # Momentum diverging from trend suggests weakening conviction
    trend_dir = 1 if features['ema_slope'] > 0 else -1
    momentum_dir = 1 if features['momentum_score'] > 0 else -1
    momentum_diverges = trend_dir != momentum_dir and abs(features['momentum_score']) > 0.3
    
    # Reject only when BOTH conditions occur together
    if wick_dominant and momentum_diverges:
        return "skip"
    return prediction