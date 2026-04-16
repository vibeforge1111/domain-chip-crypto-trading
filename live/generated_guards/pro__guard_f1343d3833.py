def guard(features: dict, prediction: str) -> str:
    """Reject trades when candle shows weak commitment in volatile conditions."""
    # Doji-like candle with low momentum and high volatility is a bad setup
    if (features.get('body_ratio', 1) < 0.2 and 
        features.get('momentum_score', 0.5) < 0.35 and 
        features.get('atr_ratio', 1) > 1.2):
        return "skip"
    return prediction