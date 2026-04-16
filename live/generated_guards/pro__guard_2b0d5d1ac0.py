def guard(features: dict, prediction: str) -> str:
    """Reject trades at extreme overbought/oversold conditions using BB and Stochastic."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # Reject long when overbought: BB upper band + stoch > 80
    if prediction == "long" and bb_pct_b > 0.9 and stoch_k > 80:
        return "skip"
    
    # Reject short when oversold: BB lower band + stoch < 20
    if prediction == "short" and bb_pct_b < 0.1 and stoch_k < 20:
        return "skip"
    
    # Additional filter: avoid longs when price is too far below VWAP (weakness)
    if prediction == "long" and vwap_deviation < -0.02:
        return "skip"
    
    return prediction