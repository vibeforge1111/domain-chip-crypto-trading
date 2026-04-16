def guard(features: dict, prediction: str) -> str:
    """Reject signals at Bollinger Band extremes during low volatility (potential false breakouts)."""
    at_extreme = features["bb_pct_b"] > 0.95 or features["bb_pct_b"] < 0.05
    low_volatility = features["volatility_regime"] < 0.3
    
    if at_extreme and low_volatility:
        return "skip"
    
    return prediction