def guard(features: dict, prediction: str) -> str:
    # Filter false compression breakouts: tight bands + extreme position + momentum exhaustion
    if features['bb_width'] < 0.02:
        if features['bb_pct_b'] < 0.15 or features['bb_pct_b'] > 0.85:
            if features['stoch_k'] > 80 or features['stoch_k'] < 20:
                return "skip"
    return prediction