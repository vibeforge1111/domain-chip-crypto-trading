def guard(features: dict, prediction: str) -> str:
    """Reject trades at extreme overbought/oversold conditions using BB and Stoch."""
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Long trades: reject if overbought (BB upper band + Stoch >80)
    if prediction == "long" and bb > 0.85 and stoch > 80:
        return "skip"
    
    # Short trades: reject if oversold (BB lower band + Stoch <20)
    if prediction == "short" and bb < 0.15 and stoch < 20:
        return "skip"
    
    return prediction