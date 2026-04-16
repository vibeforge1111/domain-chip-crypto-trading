def guard(features: dict, prediction: str) -> str:
    """Reject trades where strong trend meets rejection candle (long wick)."""
    # Strong trend + long wick = potential reversal/rejection
    if features['trend_strength'] > 0.6 and (features['upper_wick_ratio'] > 0.4 or features['lower_wick_ratio'] > 0.4):
        return "skip"
    # Extreme RSI with contradicting momentum signals
    if features['rsi_14'] > 70 and features['momentum_score'] < -0.2:
        return "skip"
    if features['rsi_14'] < 30 and features['momentum_score'] > 0.2:
        return "skip"
    return prediction