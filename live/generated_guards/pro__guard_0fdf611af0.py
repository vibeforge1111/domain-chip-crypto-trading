def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) > 20:
        confirmations += 1
    
    # VWAP confirmation
    if features.get("vwap_deviation", 0) > 0:
        confirmations += 1
    
    # RSI confirmation
    if features.get("rsi_14", 50) > 40:
        confirmations += 1
    
    # BB position confirmation
    if features.get("bb_pct_b", 0.5) < 0.3:
        confirmations += 1
    
    if confirmations >= 2:
        return prediction
    return "skip"