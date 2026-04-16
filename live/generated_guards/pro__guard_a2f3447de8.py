def guard(features: dict, prediction: str) -> str:
    # Filter when high volume but low volatility expansion (potential fakeout)
    if prediction in ["long", "short"]:
        vol_ratio = features.get("volume_ratio", 1.0)
        atr_ratio = features.get("atr_ratio", 1.0)
        rsi = features.get("rsi_14", 50)
        
        # High volume + low ATR expansion + neutral RSI = chop/fakeout
        if vol_ratio > 1.5 and atr_ratio < 0.8 and 40 < rsi < 60:
            return "skip"
        
        # RSI at extremes with conflicting momentum
        ema_slope = features.get("ema_slope", 0)
        if prediction == "long" and rsi > 70 and ema_slope < 0:
            return "skip"
        if prediction == "short" and rsi < 30 and ema_slope > 0:
            return "skip"
    
    return prediction