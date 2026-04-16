def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum and RSI disagree (divergence signal)."""
    if prediction == "skip":
        return prediction
    
    rsi = features.get("rsi_14", 50)
    momentum = features.get("momentum_score", 0)
    
    # Bullish divergence: RSI oversold but momentum still negative
    if rsi < 35 and momentum < -0.1:
        return "skip"
    
    # Bearish divergence: RSI overbought but momentum still positive
    if rsi > 65 and momentum > 0.1:
        return "skip"
    
    return prediction