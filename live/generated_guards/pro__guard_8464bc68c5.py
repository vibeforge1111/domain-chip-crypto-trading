def guard(features: dict, prediction: str) -> str:
    # Detect false compression: high ATR but narrow BBs signals pending volatility expansion
    if features.get('atr_ratio', 0) > 1.2 and features.get('bb_width', 1) < 0.55:
        return "skip"
    return prediction