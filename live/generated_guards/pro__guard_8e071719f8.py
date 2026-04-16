def guard(features: dict, prediction: str) -> str:
    """Filter trades based on momentum-divergence and consolidation patterns."""
    rsi = features.get("rsi_14", 50)
    bb_pos = features.get("bb_position", 0.5)
    bb_width = features.get("bb_width", 0.02)
    ema_slope = features.get("ema_slope", 0)
    trend_strength = features.get("trend_strength", 0.5)
    volume_ratio = features.get("volume_ratio", 1.0)
    momentum = features.get("momentum_score", 0)
    
    # Skip if RSI extreme and BB at opposite extreme (reversal trap)
    if (rsi > 70 or rsi < 30) and ((bb_pos > 0.9 and rsi > 60) or (bb_pos < 0.1 and rsi < 40)):
        return "skip"
    
    # Skip if consolidating in high volatility without trend
    if bb_width > 1.5 and abs(ema_slope) < 0.001 and trend_strength < 0.3:
        return "skip"
    
    # Skip if momentum diverges from trend direction
    if prediction == "long" and momentum < -0.3 and ema_slope > 0:
        return "skip"
    if prediction == "short" and momentum > 0.3 and ema_slope < 0:
        return "skip"
    
    return prediction