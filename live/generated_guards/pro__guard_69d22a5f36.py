def guard(features: dict, prediction: str) -> str:
    """Reject trades when price is at Bollinger Band extreme and stochastic confirms overbought/oversold."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Both indicators showing overbought (top of bands + stoch > 80)
    overbought = bb_pct_b > 0.85 and stoch_k > 80
    # Both indicators showing oversold (bottom of bands + stoch < 20)
    oversold = bb_pct_b < 0.15 and stoch_k < 20
    
    if prediction == "long" and overbought:
        return "skip"
    if prediction == "short" and oversold:
        return "skip"
    
    return prediction