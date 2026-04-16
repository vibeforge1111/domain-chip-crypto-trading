def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using bb_pct_b and stoch_k."""
    stoch_k = features.get('stoch_k', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Reject long signals when overbought with price at upper band and weak 2h momentum
    if prediction == "long" and stoch_k > 80 and bb_pct_b > 0.85 and rsi_2h < 50:
        return "skip"
    
    # Reject short signals when oversold with price at lower band and strong 2h support
    if prediction == "short" and stoch_k < 20 and bb_pct_b < 0.15 and rsi_2h > 50:
        return "skip"
    
    return prediction