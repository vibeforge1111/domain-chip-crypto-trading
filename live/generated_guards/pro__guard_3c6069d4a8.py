def guard(features: dict, prediction: str) -> str:
    # True compression detection: tight BB + low ATR
    if features['bb_width'] < 0.055 and features['atr_ratio'] < 0.7:
        # Skip if stochastics overextended (false compression signal)
        if features['stoch_k'] > 85 or features['stoch_k'] < 15:
            return "skip"
        # Skip if 2h RSI in extreme territory
        if features['rsi_2h'] > 72 or features['rsi_2h'] < 28:
            return "skip"
    return prediction