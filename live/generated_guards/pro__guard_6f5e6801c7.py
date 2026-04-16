def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Long confirmation signals
    if features.get('stoch_k', 50) < 40:
        confirmations += 1
    if features.get('obv_slope', 0) > 0:
        confirmations += 1
    if features.get('macd_histogram', 0) > 0:
        confirmations += 1
    if features.get('bb_pct_b', 0.5) < 0.8:
        confirmations += 1
    if features.get('rsi_2h', 50) < 65:
        confirmations += 1
    
    # Short confirmation signals
    if features.get('stoch_k', 50) > 60:
        confirmations += 1
    if features.get('obv_slope', 0) < 0:
        confirmations += 1
    if features.get('macd_histogram', 0) < 0:
        confirmations += 1
    if features.get('bb_pct_b', 0.5) > 0.2:
        confirmations += 1
    
    return "skip" if confirmations < 2 else prediction