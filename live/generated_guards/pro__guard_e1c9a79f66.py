def guard(features: dict, prediction: str) -> str:
    vwap = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # VWAP and momentum disagreement filter
    vwap_aligned = (vwap > 0.003 and momentum > 0) or (vwap < -0.003 and momentum < 0)
    strong_disagreement = abs(vwap) > 0.005 and abs(momentum) > 0.4
    
    # Stochastic confirmation of momentum
    momentum_confirmed = (momentum > 0 and stoch_k > 40) or (momentum < 0 and stoch_k < 60)
    
    if strong_disagreement and not momentum_confirmed:
        return "skip"
    
    return prediction