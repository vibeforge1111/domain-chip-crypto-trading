def guard(features: dict, prediction: str) -> str:
    """Detect false compression: tight bands + low ATR but momentum divergence."""
    # False compression trap: narrow bands with extreme stoch and no volume confirmation
    if features['bb_width'] < 0.02 and features['atr_ratio'] < 0.8:
        # Stochastic extreme with bearish OBV slope suggests squeeze trap
        if (features['stoch_k'] > 80 or features['stoch_k'] < 20) and features['obv_slope'] < 0:
            return "skip"
    return prediction