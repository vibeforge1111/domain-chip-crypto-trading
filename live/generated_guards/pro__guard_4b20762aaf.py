def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme zones."""
    bb = features.get("bb_pct_b", 0.5)
    rsi = features.get("rsi_14", 50)
    
    # Long only at lower band extreme, short only at upper band extreme
    if prediction == "long" and (bb >= 0.05 or rsi < 30):
        return "skip"
    if prediction == "short" and (bb <= 0.95 or rsi > 70):
        return "skip"
    
    return prediction