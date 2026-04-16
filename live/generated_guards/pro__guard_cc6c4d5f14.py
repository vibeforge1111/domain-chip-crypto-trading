def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum diverges across timeframes."""
    rsi_14 = features.get('rsi_14', 50)
    rsi_2h = features.get('rsi_2h', 50)
    stoch_k = features.get('stoch_k', 50)
    bb_position = features.get('bb_position', 0.5)
    
    # Large RSI divergence between timeframes suggests momentum is unstable
    rsi_div = abs(rsi_14 - rsi_2h)
    if rsi_div > 25:
        return "skip"
    
    # Reject long if RSI already overbought and near upper BB
    if prediction == "long" and rsi_14 > 65 and bb_position > 0.85:
        return "skip"
    
    # Reject short if RSI already oversold and near lower BB
    if prediction == "short" and rsi_14 < 35 and bb_position < 0.15:
        return "skip"
    
    return prediction