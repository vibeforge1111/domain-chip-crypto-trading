def guard(features: dict, prediction: str) -> str:
    # Detect false compression: low bb_width with price at band extremes and extreme stoch
    bb_width = features.get('bb_width', 1)
    bb_compressed = bb_width < 0.02
    
    if bb_compressed:
        bb_extreme = features.get('bb_pct_b', 0.5) < 0.15 or features.get('bb_pct_b', 0.5) > 0.85
        stoch_extreme = features.get('stoch_k', 50) < 20 or features.get('stoch_k', 50) > 80
        
        # False compression: compressed bands + extreme price position + stoch exhaustion
        if bb_extreme and stoch_extreme:
            return "skip"
    
    return prediction