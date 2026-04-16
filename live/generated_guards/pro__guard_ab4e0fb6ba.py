def guard(features: dict, prediction: str) -> str:
    """Filter trades with weak momentum divergence from trend strength."""
    if features.get('body_ratio', 0) < 0.2 and features.get('momentum_score', 0) < 0.3:
        return "skip"
    if features.get('rsi_14', 50) > 70 and features.get('ema_slope', 0) < 0 and prediction == "long":
        return "skip"
    if features.get('rsi_14', 50) < 30 and features.get('ema_slope', 0) > 0 and prediction == "short":
        return "skip"
    return prediction