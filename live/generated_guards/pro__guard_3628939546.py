def guard(features: dict, prediction: str) -> str:
    """Filter trades to only allow entries at extreme Bollinger Band positions."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Only allow trades when bb_pct_b is in extreme zones with stochastic confirmation
    if bb_pct_b < 0.05:
        # Lower band extreme - confirm long entries with stoch exiting oversold
        if prediction == "long" and stoch_k > 20:
            return prediction
        return "skip"
    elif bb_pct_b > 0.95:
        # Upper band extreme - confirm short entries with stoch exiting overbought
        if prediction == "short" and stoch_k < 80:
            return prediction
        return "skip"
    
    # Non-extreme BB position - reject
    return "skip"