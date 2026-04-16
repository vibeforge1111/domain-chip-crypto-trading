def guard(features: dict, prediction: str) -> str:
    # False compression: tight BB but elevated ATR (breakout trap)
    if features['bb_width'] < 0.02 and features['atr_ratio'] > 1.2:
        return "skip"
    
    # Stochastic divergence during compression signals weak move
    if features['bb_width'] < 0.025 and abs(features['stoch_k'] - features['stoch_d']) > 15:
        return "skip"
    
    # Wide RSI conflict with tight positioning warns of reversal
    if abs(features['rsi_2h'] - features['rsi_14']) > 25 and features['bb_pct_b'] > 0.85:
        return "skip"
    
    return prediction