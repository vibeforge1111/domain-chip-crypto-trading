def guard(features: dict, prediction: str) -> str:
    # Skip if ATR expands significantly but BB width contracts (volatility squeeze = likely false break)
    if features.get('atr_ratio', 0) > 1.5 and features.get('bb_width', 0) < 0.25:
        return "skip"
    
    return prediction