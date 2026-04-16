def guard(features: dict, prediction: str) -> str:
    """Skip when RSI extremes conflict with momentum direction (divergence)."""
    rsi_14 = features.get('rsi_14', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    momentum_score = features.get('momentum_score', 0)
    
    # Long: price at upper band but momentum diverging bearish
    if prediction == "long" and rsi_14 > 70 and bb_pct_b > 0.85 and momentum_score < 0:
        return "skip"
    
    # Short: price at lower band but momentum diverging bullish
    if prediction == "short" and rsi_14 < 30 and bb_pct_b < 0.15 and momentum_score > 0:
        return "skip"
    
    return prediction