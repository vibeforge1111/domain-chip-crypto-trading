def guard(features: dict, prediction: str) -> str:
    """Filter trades when price is at extreme Bollinger Band position with low volume."""
    bb_pos = features['bb_position']
    vol_ratio = features['volume_ratio']
    
    # Price at band extremes with weak volume suggests weak conviction
    if (bb_pos > 0.9 or bb_pos < 0.1) and vol_ratio < 0.5:
        return "skip"
    return prediction