def guard(features: dict, prediction: str) -> str:
    """Reject trades where price reaches band extremes without momentum confirmation."""
    bb_pos = features.get('bb_position', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi = features.get('rsi_14', 50)
    momentum = features.get('momentum_score', 0)
    
    # Long signal: reject if overextended at upper band without momentum
    if prediction == "long" and bb_pos > 0.9 and rsi > 70 and momentum < 0.3:
        return "skip"
    
    # Short signal: reject if oversold at lower band without negative momentum
    if prediction == "short" and bb_pos < 0.1 and rsi < 30 and momentum > -0.3:
        return "skip"
    
    return prediction