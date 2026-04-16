def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum diverges from trend or when entering at BB extremes with weak momentum."""
    if prediction == "skip":
        return prediction
    
    # Filter: momentum vs trend divergence
    momentum_trend_conflict = (features["momentum_score"] > 0.5 and features["trend_strength"] < -0.3) or \
                              (features["momentum_score"] < -0.5 and features["trend_strength"] > 0.3)
    
    # Filter: extreme BB position with insufficient momentum confirmation
    bb_extreme_no_confirm = (features["bb_position"] > 0.95 and features["momentum_score"] < 0.2) or \
                            (features["bb_position"] < 0.05 and features["momentum_score"] > -0.2)
    
    # Filter: high ATR but low momentum (volatile move without conviction)
    volatile_no_momentum = features["atr_ratio"] > 1.5 and abs(features["momentum_score"]) < 0.3
    
    if momentum_trend_conflict or bb_extreme_no_confirm or volatile_no_momentum:
        return "skip"
    
    return prediction