from __future__ import annotations

import json
import math
from bisect import bisect_left
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev
from typing import Any

SUPPORTED_BACKTEST_ASSETS = ("btc", "eth", "sol")
SUPPORTED_BACKTEST_TIMEFRAMES = ("4h", "1h", "15m")


def _parse_ts(raw: str) -> datetime:
    return datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(timezone.utc)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


@dataclass(frozen=True)
class Candle:
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(frozen=True)
class ContractWindow:
    contract_id: str
    open_ts: datetime
    close_ts: datetime
    reference_price_open: float
    reference_price_close: float
    settlement_direction: str


def _candles(path: Path) -> list[Candle]:
    items: list[Candle] = []
    for row in _load_jsonl(path):
        try:
            items.append(
                Candle(
                    ts=_parse_ts(str(row["ts"])),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row["volume"]),
                )
            )
        except (KeyError, TypeError, ValueError):
            continue
    return sorted(items, key=lambda item: item.ts)


def _contracts(path: Path) -> list[ContractWindow]:
    items: list[ContractWindow] = []
    for row in _load_jsonl(path):
        try:
            items.append(
                ContractWindow(
                    contract_id=str(row["contract_id"]),
                    open_ts=_parse_ts(str(row["open_ts"])),
                    close_ts=_parse_ts(str(row["close_ts"])),
                    reference_price_open=float(row["reference_price_open"]),
                    reference_price_close=float(row["reference_price_close"]),
                    settlement_direction=str(row["settlement_direction"]).lower(),
                )
            )
        except (KeyError, TypeError, ValueError):
            continue
    return sorted(items, key=lambda item: item.open_ts)


def _ema(values: list[float], period: int) -> float:
    if not values:
        return 0.0
    alpha = 2.0 / (period + 1.0)
    current = values[0]
    for value in values[1:]:
        current = alpha * value + (1.0 - alpha) * current
    return current


def _rsi(values: list[float], period: int = 14) -> float:
    if len(values) < period + 1:
        return 50.0
    gains: list[float] = []
    losses: list[float] = []
    for left, right in zip(values[-period - 1 : -1], values[-period:]):
        delta = right - left
        gains.append(max(0.0, delta))
        losses.append(max(0.0, -delta))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0.0:
        return 100.0 if avg_gain > 0.0 else 50.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def _atr(highs: list[float], lows: list[float], closes: list[float], period: int = 14) -> float:
    """Average True Range — measures true volatility including wicks and gaps."""
    if len(closes) < 2:
        return 0.0
    trs: list[float] = []
    for i in range(1, len(closes)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        trs.append(tr)
    if not trs:
        return 0.0
    atr = trs[0]
    alpha = 2.0 / (period + 1.0)
    for tr in trs[1:]:
        atr = alpha * tr + (1.0 - alpha) * atr
    return atr


def _window_candles(candles: list[Candle], candle_times: list[float], contract: ContractWindow, lookback_minutes: int = 30) -> list[Candle]:
    contract_start = contract.open_ts.timestamp()
    lookback_start = contract_start - (lookback_minutes * 60)
    left = bisect_left(candle_times, lookback_start)
    right = bisect_left(candle_times, contract_start)
    return candles[left:right]


def _feature_row(candles: list[Candle], contract: ContractWindow) -> dict[str, float]:
    closes = [item.close for item in candles]
    opens = [item.open for item in candles]
    highs = [item.high for item in candles]
    lows = [item.low for item in candles]
    volumes = [item.volume for item in candles]
    session_hour = float(contract.open_ts.hour)
    if 13 <= contract.open_ts.hour <= 16:
        session_code = 3.0
    elif 8 <= contract.open_ts.hour <= 12:
        session_code = 2.0
    elif 0 <= contract.open_ts.hour <= 7:
        session_code = 1.0
    else:
        session_code = 4.0
    if len(closes) < 5:
        return {
            "close": 0.0,
            "momentum": 0.0,
            "ema_fast": 0.0,
            "ema_slow": 0.0,
            "ema_gap_ratio": 0.0,
            "rsi": 50.0,
            "range_width": 0.0,
            "volatility": 0.0,
            "session_hour": session_hour,
            "session_code": session_code,
            "early_impulse": 0.0,
            "late_impulse": 0.0,
            "impulse_flip": 0.0,
            "compression_ratio": 1.0,
            "close_location": 0.5,
            "body_bias": 0.0,
            "volume_ratio": 1.0,
            "distance_to_recent_low": 0.0,
            "distance_to_recent_high": 0.0,
            "lower_wick_ratio": 0.0,
            "upper_wick_ratio": 0.0,
            "reclaim_strength": 0.0,
            "atr_ratio": 0.0,
            "bb_pct_b": 0.5,
            "bb_width": 0.02,
            "vwap_deviation": 0.0,
            "stoch_k": 50.0,
            "stoch_d": 50.0,
            "obv_slope": 0.0,
            "macd_histogram": 0.0,
            "adx_14": 0.0,
            "plus_di": 0.0,
            "minus_di": 0.0,
            "cci_20": 0.0,
            "keltner_pos": 0.5,
            "keltner_width": 0.02,
            "williams_r": -50.0,
            "cmf_20": 0.0,
            "hurst_exp": 0.5,
            "shannon_entropy": 0.0,
            "autocorr_1": 0.0,
            "volume_delta": 0.0,
            "rv_ratio": 1.0,
            "parkinson_vol": 0.0,
            "momentum_zscore": 0.0,
            "linreg_deviation": 0.0,
            "ou_halflife": 100.0,
        }
    ema_fast = _ema(closes[-8:], min(8, len(closes)))
    ema_slow = _ema(closes[-21:], min(21, len(closes)))
    momentum = (closes[-1] - closes[max(0, len(closes) - 6)]) / max(1.0, closes[max(0, len(closes) - 6)])
    recent_high = max(highs[-10:]) if len(highs) >= 10 else max(highs)
    recent_low = min(lows[-10:]) if len(lows) >= 10 else min(lows)
    range_width = (recent_high - recent_low) / max(1.0, closes[-1])
    returns = []
    for left, right in zip(closes[:-1], closes[1:]):
        returns.append((right - left) / max(1.0, left))
    volatility = pstdev(returns[-10:]) if len(returns) >= 2 else 0.0
    early_index = min(len(closes) - 1, 4)
    late_anchor = max(0, len(closes) - 5)
    early_impulse = (closes[early_index] - closes[0]) / max(1.0, closes[0])
    late_impulse = (closes[-1] - closes[late_anchor]) / max(1.0, closes[late_anchor])
    impulse_flip = 1.0 if early_impulse * late_impulse < 0.0 else 0.0
    full_range = max(highs) - min(lows)
    recent_range = recent_high - recent_low
    compression_ratio = recent_range / max(1.0, full_range) if full_range > 0.0 else 1.0
    close_location = (closes[-1] - recent_low) / max(1.0, recent_high - recent_low) if recent_high > recent_low else 0.5
    bodies = [(close - open_) / max(1.0, close) for open_, close in zip(opens[-5:], closes[-5:])]
    body_bias = sum(bodies) / max(1, len(bodies))
    recent_volume = sum(volumes[-5:]) / max(1, len(volumes[-5:]))
    baseline_volume = sum(volumes) / max(1, len(volumes))
    volume_ratio = recent_volume / max(1.0, baseline_volume)
    distance_to_recent_low = max(0.0, (closes[-1] - recent_low) / max(1.0, closes[-1]))
    distance_to_recent_high = max(0.0, (recent_high - closes[-1]) / max(1.0, closes[-1]))
    last_span = highs[-1] - lows[-1]
    if last_span > 0.0:
        lower_wick_ratio = max(0.0, min(opens[-1], closes[-1]) - lows[-1]) / last_span
        upper_wick_ratio = max(0.0, highs[-1] - max(opens[-1], closes[-1])) / last_span
    else:
        lower_wick_ratio = 0.0
        upper_wick_ratio = 0.0
    reclaim_strength = min(2.0, abs(late_impulse) / max(0.0002, abs(early_impulse))) if impulse_flip > 0.0 else 0.0

    # ── New confirmation indicators ─────────────────────────────

    # ATR ratio (true volatility including wicks/gaps, normalized)
    atr_raw = _atr(highs, lows, closes, period=14)
    atr_ratio = atr_raw / max(1.0, closes[-1])

    # Bollinger Band %B and width
    bb_period = 20
    if len(closes) >= bb_period:
        bb_mean = sum(closes[-bb_period:]) / bb_period
        bb_dev = (sum((c - bb_mean) ** 2 for c in closes[-bb_period:]) / bb_period) ** 0.5
        bb_upper = bb_mean + 2.0 * bb_dev
        bb_lower = bb_mean - 2.0 * bb_dev
        bb_width = (bb_upper - bb_lower) / max(1.0, bb_mean)
        bb_pct_b = (closes[-1] - bb_lower) / max(0.0001, bb_upper - bb_lower)
    else:
        bb_width = 0.02
        bb_pct_b = 0.5

    # VWAP deviation (distance from volume-weighted fair value)
    total_vol = sum(volumes)
    if len(closes) >= 5 and total_vol > 0:
        typical_prices = [(h + l + c) / 3.0 for h, l, c in zip(highs, lows, closes)]
        vwap = sum(tp * v for tp, v in zip(typical_prices, volumes)) / total_vol
        vwap_deviation = (closes[-1] - vwap) / max(1.0, closes[-1])
    else:
        vwap_deviation = 0.0

    # Stochastic %K/%D (high/low-based momentum oscillator)
    stoch_period = 14
    if len(closes) >= stoch_period:
        hh = max(highs[-stoch_period:])
        ll = min(lows[-stoch_period:])
        stoch_k = 100.0 * (closes[-1] - ll) / max(0.0001, hh - ll)
        k_vals: list[float] = []
        for j in range(min(3, len(closes) - stoch_period + 1)):
            idx = len(closes) - 1 - j
            ph = highs[max(0, idx - stoch_period + 1) : idx + 1]
            pl = lows[max(0, idx - stoch_period + 1) : idx + 1]
            k_vals.append(100.0 * (closes[idx] - min(pl)) / max(0.0001, max(ph) - min(pl)))
        stoch_d = sum(k_vals) / len(k_vals) if k_vals else stoch_k
    else:
        stoch_k = 50.0
        stoch_d = 50.0

    # OBV slope (on-balance volume flow direction)
    if len(closes) >= 5:
        obv_vals: list[float] = []
        running_obv = 0.0
        for i in range(1, len(closes)):
            if closes[i] > closes[i - 1]:
                running_obv += volumes[i]
            elif closes[i] < closes[i - 1]:
                running_obv -= volumes[i]
            obv_vals.append(running_obv)
        vol_sum_5 = sum(volumes[-5:])
        obv_denom = vol_sum_5 if vol_sum_5 > 0 else 1.0
        obv_slope = (obv_vals[-1] - obv_vals[-min(5, len(obv_vals))]) / obv_denom if len(obv_vals) >= 5 else 0.0
    else:
        obv_slope = 0.0

    # MACD histogram (momentum acceleration/deceleration)
    if len(closes) >= 26:
        macd_fast_ema = _ema(closes[-12:], 12)
        macd_slow_ema = _ema(closes[-26:], 26)
        macd_line = macd_fast_ema - macd_slow_ema
        macd_vals: list[float] = []
        for i in range(max(0, len(closes) - 9), len(closes)):
            mf = _ema(closes[max(0, i - 11) : i + 1], min(12, i + 1))
            ms = _ema(closes[max(0, i - 25) : i + 1], min(26, i + 1))
            macd_vals.append(mf - ms)
        macd_signal = _ema(macd_vals, min(9, len(macd_vals))) if macd_vals else macd_line
        macd_histogram = (macd_line - macd_signal) / max(1.0, closes[-1])
    else:
        macd_histogram = 0.0

    # ── Forge indicators (Strategy Forge Phase 1) ────────────────

    # ADX / DMI — trend strength + directional movement (14-period)
    if len(closes) >= 15:
        plus_dm_list: list[float] = []
        minus_dm_list: list[float] = []
        tr_list: list[float] = []
        for i in range(1, len(closes)):
            up_move = highs[i] - highs[i - 1]
            down_move = lows[i - 1] - lows[i]
            plus_dm_list.append(up_move if up_move > down_move and up_move > 0 else 0.0)
            minus_dm_list.append(down_move if down_move > up_move and down_move > 0 else 0.0)
            tr_list.append(max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1])))
        adx_p = 14
        alpha_adx = 2.0 / (adx_p + 1.0)
        sm_tr = tr_list[0]
        sm_plus = plus_dm_list[0]
        sm_minus = minus_dm_list[0]
        for j in range(1, len(tr_list)):
            sm_tr = alpha_adx * tr_list[j] + (1.0 - alpha_adx) * sm_tr
            sm_plus = alpha_adx * plus_dm_list[j] + (1.0 - alpha_adx) * sm_plus
            sm_minus = alpha_adx * minus_dm_list[j] + (1.0 - alpha_adx) * sm_minus
        plus_di = 100.0 * sm_plus / max(0.0001, sm_tr)
        minus_di = 100.0 * sm_minus / max(0.0001, sm_tr)
        dx = 100.0 * abs(plus_di - minus_di) / max(0.0001, plus_di + minus_di)
        adx_14 = dx  # single-point ADX approximation
    else:
        adx_14 = 0.0
        plus_di = 0.0
        minus_di = 0.0

    # CCI — Commodity Channel Index (20-period)
    cci_period = 20
    if len(closes) >= cci_period:
        tp_vals = [(h + l + c) / 3.0 for h, l, c in zip(highs[-cci_period:], lows[-cci_period:], closes[-cci_period:])]
        tp_mean = sum(tp_vals) / cci_period
        tp_mad = sum(abs(tp - tp_mean) for tp in tp_vals) / cci_period
        cci_20 = (tp_vals[-1] - tp_mean) / max(0.0001, 0.015 * tp_mad)
    else:
        cci_20 = 0.0

    # Keltner Channel — ATR-based volatility envelope
    if len(closes) >= 20:
        kc_mid = _ema(closes[-20:], 20)
        kc_atr = _atr(highs[-21:], lows[-21:], closes[-21:], period=10)
        kc_upper = kc_mid + 2.0 * kc_atr
        kc_lower = kc_mid - 2.0 * kc_atr
        kc_span = kc_upper - kc_lower
        keltner_pos = (closes[-1] - kc_lower) / max(0.0001, kc_span)
        keltner_width = kc_span / max(1.0, kc_mid)
    else:
        keltner_pos = 0.5
        keltner_width = 0.02

    # Williams %R — fast momentum oscillator (14-period)
    wr_period = 14
    if len(closes) >= wr_period:
        wr_hh = max(highs[-wr_period:])
        wr_ll = min(lows[-wr_period:])
        williams_r = -100.0 * (wr_hh - closes[-1]) / max(0.0001, wr_hh - wr_ll)
    else:
        williams_r = -50.0

    # CMF — Chaikin Money Flow (20-period)
    cmf_period = 20
    if len(closes) >= cmf_period:
        cmf_num = 0.0
        cmf_den = 0.0
        for ci in range(-cmf_period, 0):
            hl_range = highs[ci] - lows[ci]
            mfm = ((closes[ci] - lows[ci]) - (highs[ci] - closes[ci])) / max(0.0001, hl_range)
            cmf_num += mfm * volumes[ci]
            cmf_den += volumes[ci]
        cmf_20 = cmf_num / max(1.0, cmf_den)
    else:
        cmf_20 = 0.0

    # ── Session 25: Quant indicators (Renaissance-inspired) ─────

    # Hurst exponent (R/S method, approx) — H<0.5 = mean-reverting, H>0.5 = trending
    hurst_exp = 0.5  # default: random walk
    if len(returns) >= 20:
        n_h = min(len(returns), 50)
        rs = returns[-n_h:]
        rs_mean = sum(rs) / n_h
        rs_dev = [r - rs_mean for r in rs]
        cumdev = []
        running = 0.0
        for rd in rs_dev:
            running += rd
            cumdev.append(running)
        rs_range = max(cumdev) - min(cumdev) if cumdev else 0.0
        rs_std = (sum(r ** 2 for r in rs_dev) / n_h) ** 0.5
        if rs_std > 1e-10:
            rs_stat = rs_range / rs_std
            # H = log(R/S) / log(n)
            import math as _math
            hurst_exp = max(0.0, min(1.0, _math.log(max(rs_stat, 1e-10)) / _math.log(n_h)))

    # Shannon entropy (of discretized returns) — high = unpredictable/random
    shannon_entropy = 0.0
    if len(returns) >= 10:
        n_e = min(len(returns), 50)
        ent_rets = returns[-n_e:]
        # Discretize into 5 bins
        if max(abs(r) for r in ent_rets) > 1e-10:
            mn, mx = min(ent_rets), max(ent_rets)
            bin_w = (mx - mn) / 5.0 if mx > mn else 1.0
            bins = [0] * 5
            for r in ent_rets:
                b = min(4, int((r - mn) / bin_w)) if bin_w > 0 else 2
                bins[b] += 1
            import math as _math
            for cnt in bins:
                if cnt > 0:
                    p = cnt / n_e
                    shannon_entropy -= p * _math.log(p)
            # Normalize to [0, 1] range (max entropy = log(5) ~ 1.609)
            shannon_entropy = shannon_entropy / 1.6094

    # Autocorrelation (lag 1) — serial correlation of returns
    autocorr_1 = 0.0
    if len(returns) >= 10:
        n_a = min(len(returns), 50)
        ac_rets = returns[-n_a:]
        ac_mean = sum(ac_rets) / n_a
        ac_var = sum((r - ac_mean) ** 2 for r in ac_rets) / n_a
        if ac_var > 1e-15:
            ac_cov = sum((ac_rets[i] - ac_mean) * (ac_rets[i - 1] - ac_mean) for i in range(1, n_a)) / (n_a - 1)
            autocorr_1 = max(-1.0, min(1.0, ac_cov / ac_var))

    # Estimated volume delta (buy vs sell pressure proxy)
    # Uses close position within bar to estimate buy/sell volume split
    volume_delta = 0.0
    if len(closes) >= 5:
        vd_sum = 0.0
        vd_n = min(5, len(closes))
        for vi in range(-vd_n, 0):
            bar_range = highs[vi] - lows[vi]
            if bar_range > 0:
                buy_pct = (closes[vi] - lows[vi]) / bar_range
                vd_sum += volumes[vi] * (2.0 * buy_pct - 1.0)
        vd_sum /= max(1.0, sum(volumes[-vd_n:]))
        volume_delta = max(-1.0, min(1.0, vd_sum))

    # Realized vol ratio (short/long) — regime shift detector
    rv_ratio = 1.0
    if len(returns) >= 20:
        rv_short = (sum(r ** 2 for r in returns[-5:]) / 5) ** 0.5
        rv_long = (sum(r ** 2 for r in returns[-20:]) / 20) ** 0.5
        rv_ratio = rv_short / max(1e-10, rv_long)

    # Parkinson volatility (high-low based, more efficient than close-close)
    parkinson_vol = 0.0
    if len(highs) >= 5:
        import math as _math
        pk_n = min(len(highs), 20)
        pk_sum = 0.0
        for pi in range(-pk_n, 0):
            if highs[pi] > 0 and lows[pi] > 0:
                hl_log = _math.log(highs[pi] / max(lows[pi], 1e-10))
                pk_sum += hl_log ** 2
        parkinson_vol = (pk_sum / (4.0 * pk_n * _math.log(2.0))) ** 0.5

    # Session 26: Quant research expansion features
    # Momentum Z-score (velocity extremes, orthogonal to RSI level)
    momentum_zscore = 0.0
    if len(returns) >= 20:
        mom_window = returns[-20:]
        mom_mean = sum(mom_window) / len(mom_window)
        mom_std = (sum((r - mom_mean) ** 2 for r in mom_window) / len(mom_window)) ** 0.5
        momentum_zscore = (momentum - mom_mean) / mom_std if mom_std > 1e-10 else 0.0
        momentum_zscore = max(-5.0, min(5.0, momentum_zscore))

    # Linear regression deviation (distance from 20-bar trend line, ATR-normalized)
    linreg_deviation = 0.0
    if len(closes) >= 20:
        lr_n = 20
        lr_closes = closes[-lr_n:]
        lr_x_mean = (lr_n - 1) / 2.0
        lr_y_mean = sum(lr_closes) / lr_n
        lr_num = sum((i - lr_x_mean) * (y - lr_y_mean) for i, y in enumerate(lr_closes))
        lr_den = sum((i - lr_x_mean) ** 2 for i in range(lr_n))
        lr_slope = lr_num / lr_den if lr_den > 0 else 0.0
        lr_value = lr_y_mean + lr_slope * (lr_n - 1 - lr_x_mean)
        linreg_deviation = (closes[-1] - lr_value) / max(atr_raw, 1e-10)
        linreg_deviation = max(-5.0, min(5.0, linreg_deviation))

    # Ornstein-Uhlenbeck half-life (mean-reversion speed, 20-bar AR(1))
    ou_halflife = 100.0
    if len(closes) >= 21:
        ou_y = [closes[-(20 - i)] - closes[-(21 - i)] for i in range(20)]
        ou_x = [closes[-(21 - i)] for i in range(20)]
        ou_x_mean = sum(ou_x) / len(ou_x)
        ou_num = sum((xi - ou_x_mean) * yi for xi, yi in zip(ou_x, ou_y))
        ou_den = sum((xi - ou_x_mean) ** 2 for xi in ou_x) + 1e-10
        ou_beta = ou_num / ou_den
        if ou_beta < -1e-6:
            import math as _math2
            ou_halflife = max(1.0, min(100.0, -_math2.log(2.0) / ou_beta))

    return {
        "close": closes[-1],
        "momentum": momentum,
        "ema_fast": ema_fast,
        "ema_slow": ema_slow,
        "ema_gap_ratio": (ema_fast - ema_slow) / max(1.0, closes[-1]),
        "rsi": _rsi(closes),
        "range_width": range_width,
        "volatility": volatility,
        "session_hour": session_hour,
        "session_code": session_code,
        "early_impulse": early_impulse,
        "late_impulse": late_impulse,
        "impulse_flip": impulse_flip,
        "compression_ratio": compression_ratio,
        "close_location": close_location,
        "body_bias": body_bias,
        "volume_ratio": volume_ratio,
        "distance_to_recent_low": distance_to_recent_low,
        "distance_to_recent_high": distance_to_recent_high,
        "lower_wick_ratio": lower_wick_ratio,
        "upper_wick_ratio": upper_wick_ratio,
        "reclaim_strength": reclaim_strength,
        "atr_ratio": atr_ratio,
        "bb_pct_b": bb_pct_b,
        "bb_width": bb_width,
        "vwap_deviation": vwap_deviation,
        "stoch_k": stoch_k,
        "stoch_d": stoch_d,
        "obv_slope": obv_slope,
        "macd_histogram": macd_histogram,
        "adx_14": adx_14,
        "plus_di": plus_di,
        "minus_di": minus_di,
        "cci_20": cci_20,
        "keltner_pos": keltner_pos,
        "keltner_width": keltner_width,
        "williams_r": williams_r,
        "cmf_20": cmf_20,
        # Session 25: Quant indicators
        "hurst_exp": hurst_exp,
        "shannon_entropy": shannon_entropy,
        "autocorr_1": autocorr_1,
        "volume_delta": volume_delta,
        "rv_ratio": rv_ratio,
        "parkinson_vol": parkinson_vol,
        # Session 26: Quant research expansion
        "momentum_zscore": momentum_zscore,
        "linreg_deviation": linreg_deviation,
        "ou_halflife": ou_halflife,
    }


def _wider_context(candles: list[Candle], candle_times: list[float], contract: ContractWindow) -> dict[str, float]:
    """Compute 2-hour wider context features for Session 15c guards."""
    wide = _window_candles(candles, candle_times, contract, lookback_minutes=120)
    if len(wide) < 10:
        return {"trend_2h": 0.0, "pos_in_2h": 0.5, "vol_2h": 0.0, "rsi_2h": 50.0}
    closes = [c.close for c in wide]
    highs_w = [c.high for c in wide]
    lows_w = [c.low for c in wide]
    trend_2h = (closes[-1] - closes[0]) / max(1.0, closes[0])
    range_hi = max(highs_w)
    range_lo = min(lows_w)
    pos_in_2h = (closes[-1] - range_lo) / max(1.0, range_hi - range_lo) if range_hi > range_lo else 0.5
    rets = [(closes[i] - closes[i - 1]) / max(1.0, closes[i - 1]) for i in range(1, len(closes))]
    vol_2h = (sum(r ** 2 for r in rets) / len(rets)) ** 0.5 if rets else 0.0
    rsi_2h = _rsi(closes, period=14)
    return {"trend_2h": trend_2h, "pos_in_2h": pos_in_2h, "vol_2h": vol_2h, "rsi_2h": rsi_2h}


def _detected_regime(features: dict[str, float]) -> str:
    volatility = features["volatility"]
    momentum = abs(features["momentum"])
    ema_gap_ratio = abs(features["ema_gap_ratio"])
    range_width = features["range_width"]
    volume_ratio = features.get("volume_ratio", 1.0)
    compression_ratio = features.get("compression_ratio", 1.0)
    impulse_flip = features.get("impulse_flip", 0.0)
    body_bias = abs(features.get("body_bias", 0.0))
    if volatility > 0.0022 and volume_ratio > 1.2:
        return "fear_shock"
    if (volatility > 0.0015 or range_width > 0.008) and volume_ratio > 1.15 and impulse_flip > 0.0:
        return "fear_shock"
    if compression_ratio < 0.5 and volume_ratio < 0.95 and body_bias < 0.0003:
        return "compression"
    if volatility < 0.0005 and range_width < 0.003 and compression_ratio < 0.55:
        return "compression"
    if volatility > 0.0018 or range_width > 0.01:
        return "high_vol"
    if ema_gap_ratio > 0.0012 and momentum > 0.002:
        return "trend"
    if volatility < 0.0007 and range_width < 0.004:
        return "range"
    return "event_driven"


def _apply_indicator_guards(
    mutations: dict[str, str],
    features: dict[str, float],
    prefix: str,
    likely_dir: str,
) -> bool:
    """Apply 5 standard indicator guards (ADX, CCI, Keltner, Williams %R, CMF).

    Returns True if the trade should be SKIPPED, False if it passes all guards.
    Each guard is keyed by ``{prefix}_adx_guard``, ``{prefix}_cci_guard``, etc.
    """
    # ADX/DMI — trend strength filter
    adx_guard = mutations.get(f"{prefix}_adx_guard", "")
    if adx_guard:
        adx_val = features.get("adx_14", 0.0)
        if adx_guard == "skip_no_trend" and adx_val < 20.0:
            return True
        if adx_guard == "skip_strong_trend" and adx_val > 40.0:
            return True
        if adx_guard == "skip_extreme_trend" and adx_val > 50.0:
            return True
        if adx_guard == "require_di_aligned":
            p_di = features.get("plus_di", 0.0)
            m_di = features.get("minus_di", 0.0)
            if likely_dir == "up" and m_di > p_di:
                return True
            if likely_dir == "down" and p_di > m_di:
                return True
    # CCI — mean reversion dead zone filter
    cci_guard = mutations.get(f"{prefix}_cci_guard", "")
    if cci_guard:
        cci_val = features.get("cci_20", 0.0)
        if cci_guard == "skip_dead_zone" and -50.0 < cci_val < 50.0:
            return True
        if cci_guard == "skip_narrow" and -100.0 < cci_val < 100.0:
            return True
        if cci_guard == "skip_extreme" and (cci_val > 200.0 or cci_val < -200.0):
            return True
        if cci_guard == "require_aligned":
            if likely_dir == "up" and cci_val > -20.0:
                return True
            if likely_dir == "down" and cci_val < 20.0:
                return True
    # Keltner Channel — position and width filter
    keltner_guard = mutations.get(f"{prefix}_keltner_guard", "")
    if keltner_guard:
        kp = features.get("keltner_pos", 0.5)
        kw = features.get("keltner_width", 0.02)
        if keltner_guard == "skip_inside" and 0.2 < kp < 0.8:
            return True
        if keltner_guard == "skip_narrow_channel" and kw < 0.01:
            return True
        if keltner_guard == "require_extreme":
            if likely_dir == "up" and kp > 0.15:
                return True
            if likely_dir == "down" and kp < 0.85:
                return True
    # Williams %R — fast momentum filter
    williams_guard = mutations.get(f"{prefix}_williams_guard", "")
    if williams_guard:
        wr_val = features.get("williams_r", -50.0)
        if williams_guard == "skip_neutral" and -80.0 < wr_val < -20.0:
            return True
        if williams_guard == "skip_wide_neutral" and -70.0 < wr_val < -30.0:
            return True
        if williams_guard == "require_aligned":
            if likely_dir == "up" and wr_val > -80.0:
                return True
            if likely_dir == "down" and wr_val < -20.0:
                return True
    # CMF — volume flow direction filter
    cmf_guard = mutations.get(f"{prefix}_cmf_guard", "")
    if cmf_guard:
        cmf_val = features.get("cmf_20", 0.0)
        if cmf_guard == "require_aligned":
            if likely_dir == "up" and cmf_val < 0.0:
                return True
            if likely_dir == "down" and cmf_val > 0.0:
                return True
        if cmf_guard == "require_strong":
            if likely_dir == "up" and cmf_val < 0.05:
                return True
            if likely_dir == "down" and cmf_val > -0.05:
                return True
        if cmf_guard == "skip_weak_flow" and -0.05 < cmf_val < 0.05:
            return True
    return False


def _signal(mutations: dict[str, str], features: dict[str, float]) -> str:
    doctrine_id = mutations.get("doctrine_id", "")
    strategy_id = mutations.get("strategy_id", "")
    # Doctrine card strategy_ids → existing code paths (alias routing)
    _STRATEGY_ALIAS = {
        "breakout_open_interest_confirmation": "bollinger_squeeze_breakout",
        "range_reclaim_scalp": "range_extreme_fade",
        "ema_pullback_long": "trend_pullback_entry",
        "fear_shock_avoidance": "funding_mean_revert",
        "breakout_quality_gate": "bollinger_squeeze_breakout",
    }
    strategy_id = _STRATEGY_ALIAS.get(strategy_id, strategy_id)
    desired_regime = mutations.get("market_regime", "")
    activation_profile = mutations.get("activation_profile", "base")
    execution_buffer = mutations.get("execution_buffer", "base")
    late_sample_guard = mutations.get("late_sample_guard", "off")
    drawdown_guard = mutations.get("drawdown_guard", "off")
    session_profile = mutations.get("session_profile", "all")
    impulse_profile = mutations.get("impulse_profile", "base")
    compression_profile = mutations.get("compression_profile", "base")
    reversal_confirmation = mutations.get("reversal_confirmation", "base")
    no_trade_window = mutations.get("no_trade_window", "off")
    range_edge_profile = mutations.get("range_edge_profile", "base")
    wick_profile = mutations.get("wick_profile", "base")
    chase_policy = mutations.get("chase_policy", "base")
    follow_through_profile = mutations.get("follow_through_profile", "base")
    catalyst_failure_mode = mutations.get("catalyst_failure_mode", "base")
    event_interpretation_policy = mutations.get("event_interpretation_policy", "base")
    volume_context_guard = mutations.get("volume_context_guard", "off")
    session_quality_filter = mutations.get("session_quality_filter", "off")
    counter_trend_guard = mutations.get("counter_trend_guard", "off")
    reclaim_guard = mutations.get("reclaim_guard", "off")
    direction_filter = mutations.get("direction_filter", "all")
    momentum = features["momentum"]
    ema_gap_ratio = features["ema_gap_ratio"]
    rsi = features["rsi"]
    range_width = features["range_width"]
    volatility = features["volatility"]
    session_hour = int(features.get("session_hour", 0.0) or 0.0)
    session_code = int(features.get("session_code", 0.0) or 0.0)
    early_impulse = features.get("early_impulse", 0.0)
    late_impulse = features.get("late_impulse", 0.0)
    impulse_flip = features.get("impulse_flip", 0.0)
    compression_ratio = features.get("compression_ratio", 1.0)
    close_location = features.get("close_location", 0.5)
    body_bias = features.get("body_bias", 0.0)
    volume_ratio = features.get("volume_ratio", 1.0)
    distance_to_recent_low = features.get("distance_to_recent_low", 0.0)
    distance_to_recent_high = features.get("distance_to_recent_high", 0.0)
    lower_wick_ratio = features.get("lower_wick_ratio", 0.0)
    upper_wick_ratio = features.get("upper_wick_ratio", 0.0)
    reclaim_strength = features.get("reclaim_strength", 0.0)
    detected_regime = _detected_regime(features)
    trend_momentum_floor = 0.0015
    trend_gap_floor = 0.0009
    breakout_range_floor = 0.0035
    breakout_momentum_floor = 0.001
    breakout_momentum_cap = 0.006
    mean_reversion_momentum_cap = 0.004
    if activation_profile == "wider":
        trend_momentum_floor = 0.0011
        trend_gap_floor = 0.0007
        breakout_range_floor = 0.0028
        breakout_momentum_floor = 0.0008
        breakout_momentum_cap = 0.0075
        mean_reversion_momentum_cap = 0.005
    elif activation_profile == "stricter":
        trend_momentum_floor = 0.0019
        trend_gap_floor = 0.0011
        breakout_range_floor = 0.0042
        breakout_momentum_floor = 0.0014
        breakout_momentum_cap = 0.0055
        mean_reversion_momentum_cap = 0.0032
    if execution_buffer == "high":
        trend_momentum_floor += 0.0004
        breakout_momentum_floor += 0.0005
        breakout_range_floor += 0.0008
        mean_reversion_momentum_cap -= 0.0006
    mean_reversion_volatility_cap = 0.0009
    mean_reversion_range_cap = 0.0055
    mean_reversion_rsi_floor = 28.0
    mean_reversion_rsi_ceiling = 72.0
    if drawdown_guard == "high":
        mean_reversion_volatility_cap = 0.00062
        mean_reversion_range_cap = 0.0041
        mean_reversion_momentum_cap = min(mean_reversion_momentum_cap, 0.0024)
        mean_reversion_rsi_floor = 22.0
        mean_reversion_rsi_ceiling = 78.0
    elif drawdown_guard == "moderate":
        mean_reversion_volatility_cap = 0.00078
        mean_reversion_range_cap = 0.0048
        mean_reversion_momentum_cap = min(mean_reversion_momentum_cap, 0.0028)
    if late_sample_guard == "on" and (volatility > 0.0012 or range_width > 0.0085):
        return "skip"
    if detected_regime == "fear_shock" and desired_regime != "fear_shock":
        return "skip"
    if desired_regime and desired_regime != detected_regime:
        if not (desired_regime == "event_driven" and detected_regime == "high_vol"):
            if not (desired_regime == "fear_shock" and detected_regime == "high_vol"):
                return "skip"
    if no_trade_window == "avoid_dead_zone":
        if session_code in {1, 4} and volume_ratio < 0.95:
            return "skip"
        if abs(momentum) < 0.0005 and range_width < 0.0032:
            return "skip"
    elif no_trade_window == "avoid_post_open_drift":
        if session_code == 3 and session_hour >= 16 and volume_ratio < 0.98:
            return "skip"
        if abs(late_impulse) < 0.00045 and abs(body_bias) < 0.00018:
            return "skip"
    elif no_trade_window == "avoid_reflexive_burst":
        if volatility > 0.0016 and range_width > 0.008 and abs(momentum) > 0.0028:
            return "skip"
        if volume_ratio > 1.35 and compression_ratio > 0.82:
            return "skip"
    elif no_trade_window == "avoid_chase_extension":
        # Minervini: skip extended moves (already chased, no edge)
        if abs(momentum) > 0.0022 and abs(ema_gap_ratio) > 0.0012:
            return "skip"
    elif no_trade_window == "avoid_conflict_window":
        # Elder: skip when short and long timeframes conflict
        trend_2h = features.get("trend_2h", 0.0)
        if (momentum > 0 and trend_2h < -0.0003) or (momentum < 0 and trend_2h > 0.0003):
            return "skip"
    elif no_trade_window == "avoid_low_efficiency_drift":
        # Kaufman: skip low-efficiency drift (noisy, trendless)
        if abs(ema_gap_ratio) > 0 and abs(momentum) > 0:
            efficiency = abs(ema_gap_ratio) / (abs(momentum) + 1e-9)
            if efficiency < 0.25 and abs(momentum) < 0.001:
                return "skip"
    elif no_trade_window == "avoid_false_midrange":
        # Wyckoff: skip midrange (no spring/upthrust, no edge)
        if 0.30 < close_location < 0.70 and abs(rsi - 50) < 12:
            return "skip"
    if event_interpretation_policy == "wait_for_follow_through":
        if volume_ratio > 1.15 and abs(momentum) > 0.0018:
            return "skip"
        if compression_ratio > 0.82 or abs(early_impulse) > 0.0015:
            return "skip"
    if volume_context_guard == "thin_filter":
        if volume_ratio < 0.72 and abs(momentum) < 0.001:
            return "skip"
    elif volume_context_guard == "strict_participation":
        if volume_ratio < 0.82:
            return "skip"
    if session_quality_filter == "skip_late":
        if session_code == 4:
            return "skip"
    elif session_quality_filter == "skip_asia":
        if session_code == 1:
            return "skip"
    elif session_quality_filter == "skip_toxic_hours":
        hour = int(features.get("session_hour", -1))
        if hour in {5, 6, 7, 8, 14, 15, 17, 18, 23}:
            return "skip"
    elif session_quality_filter == "skip_compression_toxic":
        hour = int(features.get("session_hour", -1))
        if hour in {3, 5, 7, 8, 11, 13, 17, 20, 21, 23}:
            return "skip"
    elif session_quality_filter == "skip_compression_toxic_v2":
        # Data-driven: hours 02 (27% WR), 12 (30% WR), 15 (0% WR), 22 (39% WR)
        hour = int(features.get("session_hour", -1))
        if hour in {2, 12, 15, 22}:
            return "skip"
    elif session_quality_filter == "active_hours_only":
        if session_code in {1, 4}:
            return "skip"
    elif session_quality_filter == "prime_sessions":
        if session_code not in {2, 3}:
            return "skip"

    # Reclaim guard: skip trades where price has already reclaimed too much
    if reclaim_guard == "capped" and reclaim_strength >= 0.9:
        return "skip"

    # ── Session 25: Quant indicator guards (Renaissance-inspired) ──
    hurst_exp = features.get("hurst_exp", 0.5)
    shannon_entropy = features.get("shannon_entropy", 0.0)
    autocorr_1 = features.get("autocorr_1", 0.0)
    volume_delta = features.get("volume_delta", 0.0)
    rv_ratio = features.get("rv_ratio", 1.0)
    parkinson_vol = features.get("parkinson_vol", 0.0)

    cr_hurst = mutations.get("cr_hurst_guard", "")
    if cr_hurst == "skip_random" and 0.4 < hurst_exp < 0.6:
        return "skip"  # random walk - no edge
    elif cr_hurst == "skip_trending" and hurst_exp > 0.65:
        return "skip"  # strong trend - bad for mean-reversion
    elif cr_hurst == "require_mean_revert" and hurst_exp > 0.45:
        return "skip"  # only trade when strongly mean-reverting

    cr_entropy = mutations.get("cr_entropy_guard", "")
    if cr_entropy == "skip_high_entropy" and shannon_entropy > 0.85:
        return "skip"  # too random/unpredictable
    elif cr_entropy == "skip_very_high" and shannon_entropy > 0.92:
        return "skip"  # extreme randomness only

    cr_autocorr = mutations.get("cr_autocorr_guard", "")
    if cr_autocorr == "skip_positive" and autocorr_1 > 0.15:
        return "skip"  # trending serial correlation - bad for fades
    elif cr_autocorr == "skip_negative" and autocorr_1 < -0.15:
        return "skip"  # mean-reverting serial correlation - bad for momentum

    cr_vd = mutations.get("cr_volume_delta_guard", "")
    if cr_vd == "skip_against_delta":
        if (momentum > 0 and volume_delta < -0.2) or (momentum < 0 and volume_delta > 0.2):
            return "skip"  # price vs volume divergence
    elif cr_vd == "require_aligned":
        if (momentum > 0 and volume_delta < 0.05) or (momentum < 0 and volume_delta > -0.05):
            return "skip"  # require volume confirms direction

    cr_rv = mutations.get("cr_rv_ratio_guard", "")
    if cr_rv == "skip_expanding" and rv_ratio > 2.0:
        return "skip"  # volatility expanding rapidly
    elif cr_rv == "skip_contracting" and rv_ratio < 0.4:
        return "skip"  # volatility collapsing

    cr_pk = mutations.get("cr_parkinson_guard", "")
    if cr_pk == "skip_high_vol" and parkinson_vol > 0.015:
        return "skip"  # extreme high-low volatility
    elif cr_pk == "skip_low_vol" and parkinson_vol < 0.001:
        return "skip"  # dead market, no movement

    if doctrine_id == "trend_regime_following":
        if detected_regime != "trend":
            return "skip"
        if chase_policy == "no_chase_after_crowded_good_news":
            if momentum > 0 and (close_location > 0.82 or volume_ratio > 1.2):
                return "skip"
            if momentum < 0 and (close_location < 0.18 or volume_ratio > 1.2):
                return "skip"
        if follow_through_profile == "delayed_confirmation":
            if abs(late_impulse) < max(0.0008, trend_momentum_floor - 0.0002):
                return "skip"
            if volume_ratio < 0.98:
                return "skip"
        if session_profile == "trend_session_alignment" and session_code not in {2, 3}:
            return "skip"
        if session_profile == "trend_session_alignment":
            trend_momentum_floor = max(0.0009, trend_momentum_floor - 0.0002)
            trend_gap_floor = max(0.0006, trend_gap_floor - 0.0001)
        if impulse_profile == "aligned_continuation":
            if early_impulse * late_impulse <= 0.0:
                return "skip"
            if abs(early_impulse) < 0.0009 or abs(late_impulse) < 0.0007:
                return "skip"
            if momentum > 0 and close_location < 0.58:
                return "skip"
            if momentum < 0 and close_location > 0.42:
                return "skip"
        if ema_gap_ratio > trend_gap_floor and momentum > trend_momentum_floor and 54 <= rsi <= 72:
            return "up"
        if ema_gap_ratio < -trend_gap_floor and momentum < -trend_momentum_floor and 28 <= rsi <= 46:
            return "down"
        return "skip"

    if doctrine_id == "mean_reversion_liquidity_reclaim":
        if detected_regime != "range":
            return "skip"
        if catalyst_failure_mode == "sell_the_news_failure_fade":
            if impulse_flip < 0.5:
                return "skip"
            if upper_wick_ratio < 0.22 and lower_wick_ratio < 0.22:
                return "skip"
            mean_reversion_momentum_cap = min(mean_reversion_momentum_cap, 0.0026)
        if session_profile == "opening_range_failure":
            if session_code != 3 or not (13 <= session_hour <= 16):
                return "skip"
            if range_width < 0.0028 or volatility < 0.00045:
                return "skip"
            mean_reversion_rsi_floor = min(mean_reversion_rsi_floor, 25.0)
            mean_reversion_rsi_ceiling = max(mean_reversion_rsi_ceiling, 75.0)
            mean_reversion_momentum_cap = min(mean_reversion_momentum_cap, 0.0028)
        if impulse_profile == "opening_reversal":
            if impulse_flip < 0.5:
                return "skip"
            if abs(early_impulse) < 0.0012 or abs(late_impulse) < 0.0008:
                return "skip"
        if reversal_confirmation == "reclaim_close":
            if early_impulse < 0.0 and (late_impulse <= 0.0 or close_location < 0.55):
                return "skip"
            if early_impulse > 0.0 and (late_impulse >= 0.0 or close_location > 0.45):
                return "skip"
        if reversal_confirmation == "edge_reclaim_close":
            if early_impulse < 0.0 and (late_impulse <= 0.0 or close_location < 0.54 or reclaim_strength < 0.4):
                return "skip"
            if early_impulse > 0.0 and (late_impulse >= 0.0 or close_location > 0.46 or reclaim_strength < 0.4):
                return "skip"
        if reversal_confirmation == "wick_reclaim_close":
            if early_impulse < 0.0 and (late_impulse <= 0.0 or close_location < 0.54 or lower_wick_ratio < 0.3):
                return "skip"
            if early_impulse > 0.0 and (late_impulse >= 0.0 or close_location > 0.46 or upper_wick_ratio < 0.3):
                return "skip"
        if late_sample_guard == "on" and (abs(momentum) > 0.0026 or volatility > mean_reversion_volatility_cap):
            return "skip"
        if drawdown_guard in {"high", "moderate"} and (volatility > mean_reversion_volatility_cap or range_width > mean_reversion_range_cap):
            return "skip"
        if drawdown_guard == "high" and abs(momentum) > 0.0019:
            return "skip"
        if drawdown_guard == "moderate" and abs(momentum) > 0.0022:
            return "skip"
        bounce_confirmation = mutations.get("bounce_confirmation", "off")
        # Counter-trend guard: skip mean-reversion calls that fight the EMA trend.
        # In a bearish micro-trend (ema_gap_ratio < 0), "up" predictions fail because
        # oversold dips are real declines, not temporary pullbacks.
        ct_ema_threshold = 0.0
        if counter_trend_guard == "gentle":
            ct_ema_threshold = 0.0006
        elif counter_trend_guard == "strict":
            ct_ema_threshold = 0.0003
        if rsi < mean_reversion_rsi_floor and -mean_reversion_momentum_cap <= momentum <= -0.0006:
            if counter_trend_guard in {"gentle", "strict"} and ema_gap_ratio < -ct_ema_threshold:
                return "skip"
            if range_edge_profile == "local_extreme_only" and distance_to_recent_low > 0.0024:
                return "skip"
            if wick_profile == "rejection_confirm" and lower_wick_ratio < 0.3:
                return "skip"
            if bounce_confirmation == "close_location" and close_location < 0.38:
                return "skip"
            if bounce_confirmation == "strong_bounce" and (close_location < 0.45 or lower_wick_ratio < 0.15):
                return "skip"
            if execution_buffer == "high" and close_location >= 0.4:
                return "skip"
            if direction_filter == "short_only":
                return "skip"
            return "up"
        if rsi > mean_reversion_rsi_ceiling and 0.0006 <= momentum <= mean_reversion_momentum_cap:
            if counter_trend_guard in {"gentle", "strict"} and ema_gap_ratio > ct_ema_threshold:
                return "skip"
            if range_edge_profile == "local_extreme_only" and distance_to_recent_high > 0.0024:
                return "skip"
            if wick_profile == "rejection_confirm" and upper_wick_ratio < 0.3:
                return "skip"
            if bounce_confirmation == "close_location" and close_location > 0.62:
                return "skip"
            if bounce_confirmation == "strong_bounce" and (close_location > 0.55 or upper_wick_ratio < 0.15):
                return "skip"
            if execution_buffer == "high" and close_location <= 0.6:
                return "skip"
            if direction_filter == "long_only":
                return "skip"
            return "down"
        return "skip"

    if doctrine_id == "breakout_volatility_expansion":
        if detected_regime not in {"high_vol", "trend"}:
            return "skip"
        if chase_policy == "no_chase_after_crowded_good_news":
            if abs(momentum) > breakout_momentum_cap * 0.88:
                return "skip"
            if momentum > 0 and close_location > 0.9 and volume_ratio > 1.15:
                return "skip"
            if momentum < 0 and close_location < 0.1 and volume_ratio > 1.15:
                return "skip"
        if follow_through_profile == "delayed_confirmation":
            if abs(late_impulse) < breakout_momentum_floor:
                return "skip"
            if volume_ratio < 1.0 or abs(body_bias) < 0.00025:
                return "skip"
        if session_profile == "squeeze_release_window":
            if session_code not in {2, 3}:
                return "skip"
            breakout_range_floor = max(0.0024, breakout_range_floor - 0.0006)
            breakout_momentum_floor = max(0.0007, breakout_momentum_floor - 0.0002)
            breakout_momentum_cap = min(0.0072, breakout_momentum_cap + 0.0004)
        if compression_profile == "preopen_squeeze":
            if compression_ratio > 0.55:
                return "skip"
            if volume_ratio < 0.9:
                return "skip"
        if impulse_profile == "expansion_follow_through":
            if abs(late_impulse) < breakout_momentum_floor or abs(body_bias) < 0.00035:
                return "skip"
            if momentum > 0 and close_location < 0.62:
                return "skip"
            if momentum < 0 and close_location > 0.38:
                return "skip"
        if range_width < breakout_range_floor and breakout_momentum_floor <= abs(momentum) <= breakout_momentum_cap and 48 <= rsi <= 78:
            return "up" if momentum > 0 else "down"
        if detected_regime == "high_vol" and volatility > 0.0012 and abs(momentum) > max(0.002, breakout_momentum_floor):
            return "up" if momentum > 0 else "down"
        return "skip"

    if doctrine_id == "risk_first_asymmetric_capture":
        if detected_regime == "high_vol" or range_width > 0.008:
            return "skip"
        if event_interpretation_policy == "wait_for_follow_through":
            if detected_regime == "event_driven":
                return "skip"
            if volume_ratio > 1.1 and abs(momentum) > 0.0016:
                return "skip"
        if strategy_id == "funding_mean_revert":
            if detected_regime == "event_driven":
                return "skip"
            if rsi < 24 and momentum < -0.002:
                return "up"
            if rsi > 76 and momentum > 0.002:
                return "down"
            return "skip"
        if late_sample_guard == "on" and volatility > 0.001:
            return "skip"
        if detected_regime == "trend" and abs(momentum) > max(0.0012, trend_momentum_floor - 0.0001) and abs(ema_gap_ratio) > max(0.0008, trend_gap_floor - 0.0001):
            return "up" if momentum > 0 else "down"
        return "skip"

    if strategy_id == "bollinger_squeeze_breakout":
        bs_regimes: set[str] = {"high_vol", "trend", "range", "compression"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            bs_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in bs_regimes:
            return "skip"
        squeeze_threshold = 0.45
        if compression_profile == "tight_squeeze":
            squeeze_threshold = 0.35
        elif compression_profile == "moderate_squeeze":
            squeeze_threshold = 0.52
        elif compression_profile == "vcp_pivot":
            squeeze_threshold = 0.38  # Minervini: tight base, very compressed
        elif compression_profile == "preopen_squeeze":
            squeeze_threshold = 0.40  # Raschke/Carter: pre-session squeeze
        if compression_ratio > squeeze_threshold:
            return "skip"
        if session_profile == "squeeze_release_window" and session_code not in {2, 3}:
            return "skip"
        if session_profile == "trend_quality_window" and session_code not in {2, 3, 4}:
            return "skip"
        bs_likely_dir = "up" if momentum > 0 else "down"
        if _apply_indicator_guards(mutations, features, "bs", bs_likely_dir):
            return "skip"
        # Doctrine card: activation_profile tightens requirements
        if activation_profile == "stricter":
            if volume_ratio < 1.0:  # stricter: require above-avg volume
                return "skip"
            breakout_momentum_floor = breakout_momentum_floor * 1.15
        # Doctrine card: impulse_profile requires follow-through
        if impulse_profile == "expansion_follow_through":
            if abs(late_impulse) < breakout_momentum_floor * 0.8:
                return "skip"  # require strong late impulse for follow-through
        elif impulse_profile == "pivot_release":
            if volume_ratio < 1.1 or abs(late_impulse) < breakout_momentum_floor * 0.6:
                return "skip"  # Minervini: need volume + impulse together
        if chase_policy == "no_chase_after_crowded_good_news":
            if abs(momentum) > breakout_momentum_cap * 0.85:
                return "skip"
        if late_sample_guard == "on" and volatility > 0.0014:
            return "skip"
        # Compression-specific entry: lower momentum threshold + volume spike
        if detected_regime == "compression":
            if volume_ratio < 0.75:
                return "skip"
            # During compression, breakouts have lower momentum but clear direction
            cr_mom_floor = breakout_momentum_floor * 0.45
            if abs(momentum) < cr_mom_floor:
                return "skip"
            if abs(momentum) > breakout_momentum_cap:
                return "skip"
            # Volume spike above baseline signals expansion beginning
            if volume_ratio > 1.05 and abs(late_impulse) > cr_mom_floor * 0.6 and abs(body_bias) > 0.00008:
                return "up" if momentum > 0 else "down"
            # Strong directional bias without volume spike
            if abs(late_impulse) > breakout_momentum_floor * 0.5 and abs(body_bias) > 0.00012:
                return "up" if momentum > 0 else "down"
            return "skip"
        # Standard path for non-compression regimes
        if volume_ratio < 0.85:
            return "skip"
        if abs(momentum) < breakout_momentum_floor * 0.9:
            return "skip"
        if abs(momentum) > breakout_momentum_cap:
            return "skip"
        if abs(late_impulse) > breakout_momentum_floor * 0.7 and abs(body_bias) > 0.00015:
            return "up" if momentum > 0 else "down"
        return "skip"

    if strategy_id == "compression_range_bounce":
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            allowed_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        else:
            allowed_regimes = {"compression"}
        if detected_regime not in allowed_regimes:
            return "skip"
        # Tighter compression = more reliable bounce
        if compression_profile == "tight_squeeze" and compression_ratio > 0.45:
            return "skip"
        if compression_profile == "moderate_tight_squeeze" and compression_ratio > 0.47:
            return "skip"
        # Data-driven guards from feature analysis (173 enriched trades)
        # upper_wick > 0.6 = 21% WR; volume_ratio > 1.7 = 0% WR
        cr_wick_guard = mutations.get("cr_wick_guard", "off")
        cr_volume_cap = mutations.get("cr_volume_cap", "off")
        cr_rsi_band = mutations.get("cr_rsi_band", "off")
        cr_compression_deadzone = mutations.get("cr_compression_deadzone", "off")
        if cr_wick_guard == "reject_high" and upper_wick_ratio > 0.6:
            return "skip"
        if cr_wick_guard == "reject_moderate" and upper_wick_ratio > 0.5:
            return "skip"
        if cr_volume_cap == "spike_skip" and volume_ratio > 1.7:
            return "skip"
        if cr_volume_cap == "moderate_cap" and volume_ratio > 1.4:
            return "skip"
        # RSI sweet spot: [21.7, 37.8] = 70.9% WR for UP trades
        # Too-oversold (RSI < 21) = 56.1% WR (price trapped, not bouncing)
        if cr_rsi_band == "sweet_spot" and rsi < 21.0:
            return "skip"
        if cr_rsi_band == "tight_sweet" and (rsi < 22.0 or rsi > 38.0):
            if close_location < 0.25:  # only apply to UP signals
                return "skip"
        # Compression ratio dead zone: [0.18, 0.27] = 47.8% WR
        if cr_compression_deadzone == "skip_mid" and 0.18 <= compression_ratio < 0.27:
            return "skip"
        # Feature interaction guards (Session 15, advanced_edge_analysis.py)
        # Pattern: multiple weak features compound into kill zones
        cr_bounce_confirm = mutations.get("cr_bounce_confirm", "off")
        cr_loose_setup = mutations.get("cr_loose_setup", "off")
        cr_body_wick_conflict = mutations.get("cr_body_wick_conflict", "off")
        # Bounce confirmation: late_impulse direction predicts success
        # High conviction finding: close_loc < med AND late_impulse > med = 90.9% WR
        # Skip UP setups where price is still falling hard (bounce hasn't started)
        if cr_bounce_confirm == "require_late_turn":
            if close_location < 0.25 and late_impulse < -0.0005:
                return "skip"
        if cr_bounce_confirm == "require_late_turn_strict":
            if close_location < 0.25 and late_impulse < 0.0:
                return "skip"
        # Loose setup: skip when both dimensions are marginal
        # Kill zone: CR > T2 AND RSI > T2 = 30.8% WR (13 trades)
        if cr_loose_setup == "skip_marginal":
            if compression_ratio > 0.38 and 28.0 < rsi < 72.0:
                return "skip"
        if cr_loose_setup == "skip_marginal_strict":
            if compression_ratio > 0.35 and 26.0 < rsi < 74.0:
                return "skip"
        # Body-wick conflict: bullish body bias + high upper wick = conflicting signals
        # Kill zone: body_bias > T2 AND upper_wick > T2 = 33.3% WR (9 trades)
        if cr_body_wick_conflict == "skip":
            if body_bias > 0.0001 and upper_wick_ratio > 0.3:
                return "skip"
        # Session 15b: Additional interaction guards from pair scan
        # Kill zone: early_impulse > T2 AND late_impulse < T1 = 33.3% WR (9 trades)
        # Intra-window momentum reversal: price went up then reversed down
        cr_impulse_reversal = mutations.get("cr_impulse_reversal", "off")
        if cr_impulse_reversal == "skip_reversal":
            if early_impulse > 0.0003 and late_impulse < -0.0005:
                return "skip"
        if cr_impulse_reversal == "skip_reversal_gentle":
            if early_impulse > 0.0005 and late_impulse < -0.0008:
                return "skip"
        # Kill zone: upper_wick > med AND distance_to_recent_high < med = 33.3% WR (18 trades)
        # Near recent high + selling wick = rejected at resistance, not a bounce
        cr_wick_near_high = mutations.get("cr_wick_near_high", "off")
        if cr_wick_near_high == "skip":
            if upper_wick_ratio > 0.20 and distance_to_recent_high < 0.0015:
                return "skip"
        if cr_wick_near_high == "skip_strict":
            if upper_wick_ratio > 0.15 and distance_to_recent_high < 0.0018:
                return "skip"
        # SOL reclaim_strength: #1 SOL discriminator (delta 0.248)
        # Weak reclaim + low momentum = bounce attempt failing
        cr_weak_reclaim = mutations.get("cr_weak_reclaim", "off")
        if cr_weak_reclaim == "skip_weak":
            if reclaim_strength < 0.25 and abs(momentum) < 0.0003:
                return "skip"
        if cr_weak_reclaim == "skip_weak_broad":
            if reclaim_strength < 0.35 and abs(momentum) < 0.0005:
                return "skip"
        # Session 15c: Wider context guards (2h lookback features)
        # U-shaped trend_2h: strong trends good, flat zone toxic (Q2-Q3 WR=0.491)
        trend_2h = features.get("trend_2h", 0.0)
        pos_in_2h = features.get("pos_in_2h", 0.5)
        # Guard 1: Downtrend + high in 2h range = false bounce at resistance
        # Kill zone: trend_2h<med AND pos_in_2h>med = WR=0.400 (25 trades)
        cr_downtrend_high_pos = mutations.get("cr_downtrend_high_pos", "off")
        if cr_downtrend_high_pos == "skip":
            if trend_2h < 0.0 and pos_in_2h > 0.52:
                return "skip"
        if cr_downtrend_high_pos == "skip_strict":
            if trend_2h < -0.0005 and pos_in_2h > 0.60:
                return "skip"
        # Guard 2: Upper wick + downtrend = rejection selling in falling market
        # Gentle guard: skip 54 trades, WR=0.662 remaining
        cr_wick_downtrend = mutations.get("cr_wick_downtrend", "off")
        if cr_wick_downtrend == "skip":
            if upper_wick_ratio > 0.30 and trend_2h < 0.0:
                return "skip"
        if cr_wick_downtrend == "skip_broad":
            if upper_wick_ratio > 0.20 and trend_2h < -0.0005:
                return "skip"
        # Guard 3: Flat/ambiguous trend zone = noise (Q2-Q3 WR=0.491)
        # WARNING: may remove too many trades for WF
        cr_flat_trend = mutations.get("cr_flat_trend", "off")
        if cr_flat_trend == "skip_flat":
            if -0.003 < trend_2h < 0.001:
                return "skip"
        if cr_flat_trend == "skip_flat_tight":
            if -0.002 < trend_2h < 0.0005:
                return "skip"
        # ── Confirmation guards (expanded indicators) ─────────────
        # Non-directional: ATR and Bollinger squeeze
        cr_atr_guard = mutations.get("cr_atr_guard", "")
        if cr_atr_guard == "skip_high_atr" and features.get("atr_ratio", 0.0) > 0.015:
            return "skip"
        if cr_atr_guard == "skip_very_high" and features.get("atr_ratio", 0.0) > 0.02:
            return "skip"
        cr_bb_squeeze = mutations.get("cr_bb_squeeze", "")
        if cr_bb_squeeze == "require_squeeze" and features.get("bb_width", 0.02) > 0.03:
            return "skip"
        if cr_bb_squeeze == "require_tight" and features.get("bb_width", 0.02) > 0.02:
            return "skip"
        # Directional guards: determine likely direction from close_location
        likely_dir = "up" if close_location < 0.5 else "down"
        cr_bb_confirm = mutations.get("cr_bb_confirm", "")
        if cr_bb_confirm == "require_extreme":
            if likely_dir == "up" and features.get("bb_pct_b", 0.5) > 0.15:
                return "skip"
            if likely_dir == "down" and features.get("bb_pct_b", 0.5) < 0.85:
                return "skip"
        if cr_bb_confirm == "require_moderate":
            if likely_dir == "up" and features.get("bb_pct_b", 0.5) > 0.30:
                return "skip"
            if likely_dir == "down" and features.get("bb_pct_b", 0.5) < 0.70:
                return "skip"
        cr_vwap_confirm = mutations.get("cr_vwap_confirm", "")
        vwap_dev = features.get("vwap_deviation", 0.0)
        if cr_vwap_confirm == "require_discount":
            if likely_dir == "up" and vwap_dev > -0.001:
                return "skip"
            if likely_dir == "down" and vwap_dev < 0.001:
                return "skip"
        if cr_vwap_confirm == "require_distance":
            if likely_dir == "up" and vwap_dev > -0.002:
                return "skip"
            if likely_dir == "down" and vwap_dev < 0.002:
                return "skip"
        cr_stoch_confirm = mutations.get("cr_stoch_confirm", "")
        stoch_k = features.get("stoch_k", 50.0)
        if cr_stoch_confirm == "require_oversold":
            if likely_dir == "up" and stoch_k > 25.0:
                return "skip"
            if likely_dir == "down" and stoch_k < 75.0:
                return "skip"
        if cr_stoch_confirm == "require_turning":
            stoch_d = features.get("stoch_d", 50.0)
            if likely_dir == "up" and (stoch_k > 30.0 or stoch_k < stoch_d):
                return "skip"
            if likely_dir == "down" and (stoch_k < 70.0 or stoch_k > stoch_d):
                return "skip"
        cr_obv_confirm = mutations.get("cr_obv_confirm", "")
        obv_sl = features.get("obv_slope", 0.0)
        if cr_obv_confirm == "require_aligned":
            if likely_dir == "up" and obv_sl < 0.0:
                return "skip"
            if likely_dir == "down" and obv_sl > 0.0:
                return "skip"
        if cr_obv_confirm == "require_strong":
            if likely_dir == "up" and obv_sl < 0.05:
                return "skip"
            if likely_dir == "down" and obv_sl > -0.05:
                return "skip"
        cr_macd_confirm = mutations.get("cr_macd_confirm", "")
        macd_h = features.get("macd_histogram", 0.0)
        if cr_macd_confirm == "require_decel":
            if likely_dir == "up" and macd_h < -0.0001:
                return "skip"
            if likely_dir == "down" and macd_h > 0.0001:
                return "skip"
        if cr_macd_confirm == "require_turn":
            if likely_dir == "up" and macd_h < 0.0:
                return "skip"
            if likely_dir == "down" and macd_h > 0.0:
                return "skip"
        cr_rsi_2h_confirm = mutations.get("cr_rsi_2h_confirm", "")
        rsi_2h = features.get("rsi_2h", 50.0)
        if cr_rsi_2h_confirm == "require_aligned":
            if likely_dir == "up" and rsi_2h > 55.0:
                return "skip"
            if likely_dir == "down" and rsi_2h < 45.0:
                return "skip"
        if cr_rsi_2h_confirm == "require_extreme":
            if likely_dir == "up" and rsi_2h > 40.0:
                return "skip"
            if likely_dir == "down" and rsi_2h < 60.0:
                return "skip"
        cr_fib_confirm = mutations.get("cr_fib_confirm", "")
        if cr_fib_confirm:
            fib_levels = [0.236, 0.382, 0.5, 0.618, 0.786]
            min_fib_dist = min(abs(close_location - f) for f in fib_levels)
            if cr_fib_confirm == "near_fib" and min_fib_dist > 0.05:
                return "skip"
            if cr_fib_confirm == "strict_fib" and min_fib_dist > 0.03:
                return "skip"
        # ── Forge indicator guards (Strategy Forge Phase 2) ──────
        if _apply_indicator_guards(mutations, features, "cr", likely_dir):
            return "skip"
        # Compression mean-reversion: price oscillates in tight band.
        # Enter at close_location extremes with RSI and body_bias confirmation.
        cr_rsi_floor = 32.0
        cr_rsi_ceiling = 68.0
        cr_close_low = 0.25
        cr_close_high = 0.75
        if drawdown_guard == "high":
            cr_rsi_floor = 25.0
            cr_rsi_ceiling = 75.0
            cr_close_low = 0.20
            cr_close_high = 0.80
        elif drawdown_guard == "moderate":
            cr_rsi_floor = 30.0
            cr_rsi_ceiling = 70.0
            cr_close_low = 0.22
            cr_close_high = 0.78
        if volume_context_guard == "thin_filter" and volume_ratio < 0.55:
            return "skip"
        if late_sample_guard == "on" and volatility > 0.0008:
            return "skip"
        # Wick confirmation: require directional wick rejection at entry
        wick_floor = 0.04 if execution_buffer == "high" else 0.0
        # Bullish: close near bottom of compression range + oversold RSI
        if close_location < cr_close_low and rsi < cr_rsi_floor:
            if body_bias <= 0.0 and lower_wick_ratio >= wick_floor:
                return "up"
        # Bearish: close near top of compression range + overbought RSI
        if close_location > cr_close_high and rsi > cr_rsi_ceiling:
            if body_bias >= 0.0 and upper_wick_ratio >= wick_floor:
                if direction_filter == "long_only":
                    return "skip"
                # Session 15d: Skip DOWN in 2h downtrend — mean reversion shouldn't
                # predict continuation. DOWN+trend_2h<0 = WR 0.482 (56 trades).
                cr_down_in_downtrend = mutations.get("cr_down_in_downtrend", "off")
                if cr_down_in_downtrend == "skip" and trend_2h < 0.0:
                    return "skip"
                if cr_down_in_downtrend == "skip_deep" and trend_2h < -0.0005:
                    return "skip"
                return "down"
        return "skip"

    if strategy_id == "event_momentum_follow":
        if detected_regime != "event_driven":
            return "skip"
        # Event-driven mean-reversion: fade impulsive moves that tend to revert.
        # Event regime has moderate volatility but impulses often overextend.
        ev_mom_floor = 0.0010
        if execution_buffer == "high":
            ev_mom_floor += 0.0003
        if volume_context_guard == "thin_filter" and volume_ratio < 0.72:
            return "skip"
        if late_sample_guard == "on" and volatility > 0.0014:
            return "skip"
        if drawdown_guard == "moderate" and range_width > 0.007:
            return "skip"
        elif drawdown_guard == "high" and range_width > 0.006:
            return "skip"
        # Fade overextended down moves (RSI oversold + momentum down)
        if rsi < 35 and momentum < -ev_mom_floor and close_location < 0.35:
            if impulse_flip > 0.0 or late_impulse > 0.0:
                return "up"
        # Fade overextended up moves (RSI overbought + momentum up)
        if rsi > 65 and momentum > ev_mom_floor and close_location > 0.65:
            if impulse_flip > 0.0 or late_impulse < 0.0:
                return "down"
        return "skip"

    if strategy_id == "wedge_exhaustion_reversal":
        if detected_regime not in {"range", "high_vol"}:
            return "skip"
        if impulse_flip < 0.5:
            return "skip"
        if abs(early_impulse) < 0.001 or abs(late_impulse) < 0.0007:
            return "skip"
        if wick_profile == "rejection_confirm":
            if early_impulse < 0 and lower_wick_ratio < 0.25:
                return "skip"
            if early_impulse > 0 and upper_wick_ratio < 0.25:
                return "skip"
        if reversal_confirmation == "reclaim_close":
            if early_impulse < 0 and close_location < 0.52:
                return "skip"
            if early_impulse > 0 and close_location > 0.48:
                return "skip"
        if late_sample_guard == "on" and volatility > 0.0016:
            return "skip"
        if drawdown_guard == "high" and range_width > 0.007:
            return "skip"
        if early_impulse < 0 and late_impulse > 0 and reclaim_strength > 0.35:
            return "up"
        if early_impulse > 0 and late_impulse < 0 and reclaim_strength > 0.35:
            return "down"
        return "skip"

    # ----------------------------------------------------------------
    # NEW STRATEGIES (151 Trading Strategies - Kakushadze & Serur)
    # ----------------------------------------------------------------

    if strategy_id == "contrarian_overextension_fade":
        co_regimes: set[str] = {"event_driven", "high_vol"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            co_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if mutations.get("co_fear_shock_allow", "off") == "allow":
            co_regimes.add("fear_shock")
        if detected_regime not in co_regimes:
            return "skip"
        co_mom_map = {"standard": 0.0015, "extreme": 0.002}
        co_mom = co_mom_map.get(mutations.get("co_momentum_threshold", "standard"), 0.0015)
        co_reclaim = 0.25 if mutations.get("co_reclaim_floor", "standard") == "standard" else 0.4
        if late_sample_guard == "on" and volatility > 0.002:
            return "skip"
        if drawdown_guard == "high" and range_width > 0.012:
            return "skip"
        if volume_context_guard == "strict_participation" and volume_ratio < 0.82:
            return "skip"
        if session_quality_filter == "skip_compression_toxic":
            if session_hour in {3, 5, 7, 8, 11, 13, 17, 20, 21, 23}:
                return "skip"
        co_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "co", co_likely_dir):
            return "skip"
        # Crash exhaustion > bounce (relaxed: late_impulse opposing momentum = turn signal)
        if momentum < -co_mom and late_impulse > 0.0001:
            if lower_wick_ratio > 0.15 or reclaim_strength > co_reclaim:
                if direction_filter != "short_only":
                    return "up"
        # Euphoria exhaustion > pullback
        if momentum > co_mom and late_impulse < -0.0001:
            if upper_wick_ratio > 0.15 or reclaim_strength > co_reclaim:
                if direction_filter != "long_only":
                    return "down"
        return "skip"

    if strategy_id == "trend_pullback_entry":
        tp_regimes: set[str] = {"trend", "event_driven", "high_vol"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            tp_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in tp_regimes:
            return "skip"
        tp_strength = 0.0004 if mutations.get("tp_trend_strength", "standard") == "standard" else 0.0008
        tp_depth_long = 0.50 if mutations.get("tp_pullback_depth", "shallow") == "shallow" else 0.40
        tp_depth_short = 0.50 if mutations.get("tp_pullback_depth", "shallow") == "shallow" else 0.60
        tp_wick = mutations.get("tp_wick_confirm", "off")
        trend_2h = features.get("trend_2h", 0.0)
        if late_sample_guard == "on" and volatility > 0.0014:
            return "skip"
        if drawdown_guard == "high" and range_width > 0.008:
            return "skip"
        if session_quality_filter == "skip_compression_toxic":
            if session_hour in {3, 5, 7, 8, 11, 13, 17, 20, 21, 23}:
                return "skip"
        # Doctrine card: impulse_profile modifies trend strength requirements
        if impulse_profile == "adaptive_efficiency":
            tp_strength = max(tp_strength, 0.0006)  # Kaufman: require stronger trend
            if abs(ema_gap_ratio) > 0 and abs(momentum) > 0:
                efficiency = abs(ema_gap_ratio) / (abs(momentum) + 1e-9)
                if efficiency < 0.3:  # low efficiency = noisy trend, skip
                    return "skip"
        # Doctrine card: session_profile filters
        if session_profile == "triple_screen_alignment" and session_code not in {2, 3}:
            return "skip"
        if session_profile == "trend_session_alignment" and session_code not in {1, 2, 3}:
            return "skip"
        tp_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "tp", tp_likely_dir):
            return "skip"
        # Doctrine card: activation_profile adjusts thresholds
        if activation_profile == "wider":
            tp_strength = tp_strength * 0.8  # wider entry: lower trend bar
        # Bullish pullback: uptrend + price pulled back
        if ema_gap_ratio > tp_strength and trend_2h > 0.0003:
            if late_impulse < 0 and close_location < tp_depth_long:
                if tp_wick == "off" or lower_wick_ratio > 0.10:
                    if direction_filter != "short_only":
                        return "up"
        # Bearish pullback: downtrend + price bounced
        if ema_gap_ratio < -tp_strength and trend_2h < -0.0003:
            if late_impulse > 0 and close_location > tp_depth_short:
                if tp_wick == "off" or upper_wick_ratio > 0.10:
                    if direction_filter != "long_only":
                        return "down"
        return "skip"

    if strategy_id == "range_extreme_fade":
        rf_regimes: set[str] = {"range", "compression"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            rf_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in rf_regimes:
            return "skip"
        rf_loc_lo = 0.15 if mutations.get("rf_location_threshold", "standard") == "standard" else 0.10
        rf_loc_hi = 0.85 if mutations.get("rf_location_threshold", "standard") == "standard" else 0.90
        rf_range = 0.002 if mutations.get("rf_range_floor", "standard") == "standard" else 0.0025
        rf_vol = mutations.get("rf_volume_guard", "off")
        if late_sample_guard == "on" and volatility > 0.001:
            return "skip"
        if rf_vol == "skip_spike" and volume_ratio > 1.5:
            return "skip"
        if drawdown_guard == "high" and range_width > 0.007:
            return "skip"
        if range_width < rf_range:
            return "skip"
        if session_quality_filter == "skip_compression_toxic":
            if session_hour in {3, 5, 7, 8, 11, 13, 17, 20, 21, 23}:
                return "skip"
        # Doctrine card: range_edge_profile tightens thresholds
        if range_edge_profile == "local_extreme_only":
            rf_loc_lo = min(rf_loc_lo, 0.10)
            rf_loc_hi = max(rf_loc_hi, 0.90)
        # Doctrine card: session_profile filters
        if session_profile == "opening_range_failure" and session_code not in {1, 2}:
            return "skip"
        if session_profile == "edge_reversal_window" and session_code not in {1, 2, 3}:
            return "skip"
        # ── Forge indicator guards (universal) ──────
        rf_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "rf", rf_likely_dir):
            return "skip"
        # At support
        if close_location < rf_loc_lo and rsi < 40 and body_bias < 0:
            if not (impulse_flip == 0 and abs(late_impulse) > 0.001):
                # Doctrine card: reversal_confirmation differentiation
                if reversal_confirmation == "wick_reclaim_close":
                    if lower_wick_ratio < 0.20 or reclaim_strength < 0.001:
                        return "skip"
                elif reversal_confirmation == "sequential_exhaustion":
                    if rsi > 25:  # stricter RSI for DeMark sequential
                        return "skip"
                elif reversal_confirmation == "edge_reclaim_close":
                    if distance_to_recent_low > 0.0008:
                        return "skip"
                elif reversal_confirmation == "candle_reversal_cluster":
                    if abs(body_bias) < 0.00012:  # need strong reversal body
                        return "skip"
                elif reversal_confirmation == "spring_upthrust_reclaim":
                    if reclaim_strength < 0.002:  # strong reclaim after spring
                        return "skip"
                # Doctrine card: wick_profile confirmation
                if wick_profile == "rejection_confirm" and lower_wick_ratio < 0.15:
                    return "skip"
                if direction_filter != "short_only":
                    return "up"
        # At resistance
        if close_location > rf_loc_hi and rsi > 60 and body_bias > 0:
            if not (impulse_flip == 0 and abs(late_impulse) > 0.001):
                # Doctrine card: reversal_confirmation differentiation
                if reversal_confirmation == "wick_reclaim_close":
                    if upper_wick_ratio < 0.20 or reclaim_strength < 0.001:
                        return "skip"
                elif reversal_confirmation == "sequential_exhaustion":
                    if rsi < 75:  # stricter RSI for DeMark sequential
                        return "skip"
                elif reversal_confirmation == "edge_reclaim_close":
                    if distance_to_recent_high > 0.0008:
                        return "skip"
                elif reversal_confirmation == "candle_reversal_cluster":
                    if abs(body_bias) < 0.00012:
                        return "skip"
                elif reversal_confirmation == "spring_upthrust_reclaim":
                    if reclaim_strength < 0.002:
                        return "skip"
                # Doctrine card: wick_profile confirmation
                if wick_profile == "rejection_confirm" and upper_wick_ratio < 0.15:
                    return "skip"
                if direction_filter != "long_only":
                    return "down"
        return "skip"

    if strategy_id == "rsi_extreme_reversion":
        if detected_regime in {"fear_shock"}:
            return "skip"
        re_rsi_lo = 22.0 if mutations.get("re_rsi_threshold", "extreme") == "extreme" else 18.0
        re_rsi_hi = 78.0 if mutations.get("re_rsi_threshold", "extreme") == "extreme" else 82.0
        re_wick = mutations.get("re_wick_confirm", "off")
        re_mom_cap = 0.004 if mutations.get("re_momentum_cap", "standard") == "standard" else 0.003
        if late_sample_guard == "on" and volatility > 0.0014:
            return "skip"
        if drawdown_guard == "high" and range_width > 0.008:
            return "skip"
        if abs(momentum) > re_mom_cap:
            return "skip"
        if session_quality_filter == "skip_compression_toxic":
            if session_hour in {3, 5, 7, 8, 11, 13, 17, 20, 21, 23}:
                return "skip"
        # ── Forge indicator guards (universal) ──────
        re_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "re", re_likely_dir):
            return "skip"
        # Oversold snap-back
        if rsi < re_rsi_lo and distance_to_recent_low < 0.001:
            if re_wick == "off" or lower_wick_ratio > 0.25:
                if direction_filter != "short_only":
                    return "up"
        # Overbought snap-back
        if rsi > re_rsi_hi and distance_to_recent_high < 0.001:
            if re_wick == "off" or upper_wick_ratio > 0.25:
                if direction_filter != "long_only":
                    return "down"
        return "skip"

    if strategy_id == "momentum_fade":
        # Fade strong momentum (crypto 15m is mean-reverting: following momentum = WR 0.43)
        mf_regimes: set[str] = {"trend", "high_vol", "event_driven"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            mf_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in mf_regimes:
            return "skip"
        mc_floor_map = {"standard": 0.0018, "aggressive": 0.0014, "conservative": 0.0022}
        mc_floor = mc_floor_map.get(mutations.get("mc_momentum_floor", "standard"), 0.0018)
        mc_rsi_band = mutations.get("mc_rsi_band", "standard")
        mc_vol = mutations.get("mc_volume_confirm", "off")
        if late_sample_guard == "on" and volatility > 0.0016:
            return "skip"
        if drawdown_guard == "high" and range_width > 0.009:
            return "skip"
        if mc_vol == "require_above_avg" and volume_ratio < 1.0:
            return "skip"
        if session_quality_filter == "skip_compression_toxic":
            if session_hour in {3, 5, 7, 8, 11, 13, 17, 20, 21, 23}:
                return "skip"
        mf_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "mf", mf_likely_dir):
            return "skip"
        # RSI bands
        if mc_rsi_band == "wide":
            rsi_lo, rsi_hi = 50.0, 80.0
        elif mc_rsi_band == "tight":
            rsi_lo, rsi_hi = 58.0, 72.0
        else:
            rsi_lo, rsi_hi = 55.0, 75.0
        # Strong bullish momentum > FADE (predict reversal down)
        if momentum > mc_floor and ema_gap_ratio > 0.0008:
            if rsi_lo <= rsi <= rsi_hi and close_location > 0.6 and body_bias > 0:
                if direction_filter != "long_only":
                    return "down"
        # Strong bearish momentum > FADE (predict reversal up)
        if momentum < -mc_floor and ema_gap_ratio < -0.0008:
            if (100 - rsi_hi) <= rsi <= (100 - rsi_lo) and close_location < 0.4 and body_bias < 0:
                if direction_filter != "short_only":
                    return "up"
        return "skip"

    if strategy_id == "ema_crossover_fade":
        # Fade fresh EMA crossovers (crypto mean-reverts after crossover: following = WR 0.45)
        ef_regimes: set[str] = {"trend", "range", "event_driven"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            ef_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in ef_regimes:
            return "skip"
        ec_ceiling = 0.0015 if mutations.get("ec_gap_ceiling", "standard") == "standard" else 0.002
        ec_impulse = mutations.get("ec_impulse_confirm", "off")
        ec_vol_floor = mutations.get("ec_volatility_floor", "off")
        if late_sample_guard == "on" and volatility > 0.0014:
            return "skip"
        if drawdown_guard == "high" and range_width > 0.008:
            return "skip"
        if compression_ratio < 0.3:
            return "skip"
        if ec_vol_floor == "minimum" and volatility < 0.0003:
            return "skip"
        if session_quality_filter == "skip_compression_toxic":
            if session_hour in {3, 5, 7, 8, 11, 13, 17, 20, 21, 23}:
                return "skip"
        ef_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "ef", ef_likely_dir):
            return "skip"
        # Bullish crossover > FADE (predict pullback down)
        if 0.0003 < ema_gap_ratio < ec_ceiling:
            if ec_impulse == "off" or late_impulse > 0.0003:
                if volume_ratio > 0.9:
                    if direction_filter != "long_only":
                        return "down"
        # Bearish crossover > FADE (predict bounce up)
        if -ec_ceiling < ema_gap_ratio < -0.0003:
            if ec_impulse == "off" or late_impulse < -0.0003:
                if volume_ratio > 0.9:
                    if direction_filter != "short_only":
                        return "up"
        return "skip"

    if strategy_id == "channel_breakout_fade":
        # Fade breakouts (crypto mean-reverts: breakout following = WR 0.39)
        cb_regimes: set[str] = {"high_vol", "event_driven", "range"}
        if detected_regime not in cb_regimes:
            return "skip"
        cb_mom = 0.0012 if mutations.get("cb_momentum_floor", "standard") == "standard" else 0.0008
        cb_vol = 0.0006 if mutations.get("cb_volatility_floor", "standard") == "standard" else 0.0004
        cb_vol_confirm = 1.05 if mutations.get("cb_volume_confirm", "standard") == "standard" else 1.15
        if late_sample_guard == "on" and volatility > 0.002:
            return "skip"
        if drawdown_guard == "high" and range_width > 0.012:
            return "skip"
        if compression_ratio < 0.3:
            return "skip"
        if impulse_flip > 0:
            return "skip"
        cb_bb_squeeze = mutations.get("cb_bb_squeeze", "")
        if cb_bb_squeeze:
            bb_w = features.get("bb_width", 0.03)
            if cb_bb_squeeze == "require_wide" and bb_w < 0.025:
                return "skip"
            if cb_bb_squeeze == "require_very_wide" and bb_w < 0.035:
                return "skip"
        if session_quality_filter == "skip_compression_toxic":
            if session_hour in {3, 5, 7, 8, 11, 13, 17, 20, 21, 23}:
                return "skip"
        # ── Forge indicator guards (universal) ──────
        cb_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "cb", cb_likely_dir):
            return "skip"
        # ── CB strategy-specific enrichment guards (P3) ──────
        cb_cmf_guard_p3 = mutations.get("cb_cmf_flow_guard", "")
        if cb_cmf_guard_p3 == "require_counter_flow":
            cmf_v = features.get("cmf_20", 0.0)
            # For fading breakouts: money flow should oppose the breakout direction
            if close_location > 0.5 and cmf_v > 0.0:
                return "skip"  # breakout up but money flowing in = don't fade
            if close_location < 0.5 and cmf_v < 0.0:
                return "skip"  # breakout down but money flowing out = don't fade
        # Bullish breakout -> FADE (predict reversal down)
        if close_location > 0.88 and momentum > cb_mom and volatility > cb_vol:
            if volume_ratio > cb_vol_confirm:
                if direction_filter != "long_only":
                    return "down"
        # Bearish breakout -> FADE (predict reversal up)
        if close_location < 0.12 and momentum < -cb_mom and volatility > cb_vol:
            if volume_ratio > cb_vol_confirm:
                if direction_filter != "short_only":
                    return "up"
        return "skip"

    if strategy_id == "multi_confirm_bounce":
        # Maximum confirmation, minimum noise: requires 3+ independent indicators
        # to agree before entry. Fewer trades but very high consistency.
        mc_regimes: set[str] = {"compression", "range"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            mc_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in mc_regimes:
            return "skip"
        if volume_context_guard == "thin_filter" and volume_ratio < 0.55:
            return "skip"
        if late_sample_guard == "on" and volatility > 0.001:
            return "skip"
        if session_quality_filter == "skip_compression_toxic":
            if session_hour in {3, 5, 7, 8, 11, 13, 17, 20, 21, 23}:
                return "skip"
        # ── MCB enrichment guards (Session 23) ──────
        mcb_atr_cap = mutations.get("mcb_atr_cap", "")
        if mcb_atr_cap:
            atr_ratio_val = features.get("atr_ratio", 0.0)
            if mcb_atr_cap == "standard" and atr_ratio_val > 0.02:
                return "skip"
            if mcb_atr_cap == "tight" and atr_ratio_val > 0.015:
                return "skip"
        mcb_confirm_threshold = mutations.get("mcb_confirm_threshold", "")
        mcb_wick_confirm = mutations.get("mcb_wick_confirm", "")
        mcb_adx_filter = mutations.get("mcb_adx_filter", "")
        if mcb_adx_filter:
            adx_val = features.get("adx_14", 0.0)
            if mcb_adx_filter == "skip_trending" and adx_val > 35.0:
                return "skip"
            if mcb_adx_filter == "skip_strong_trend" and adx_val > 45.0:
                return "skip"
        mcb_cci_filter = mutations.get("mcb_cci_filter", "")
        if mcb_cci_filter:
            cci_val = features.get("cci_20", 0.0)
            if mcb_cci_filter == "skip_neutral" and -75.0 < cci_val < 75.0:
                return "skip"
        # ── end MCB enrichment guards ──────
        # ── Forge indicator guards (universal) ──────
        mcb_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "mcb", mcb_likely_dir):
            return "skip"
        # ── MCB strategy-specific enrichment guards (P3) ──────
        mcb_stoch_guard = mutations.get("mcb_stoch_guard", "")
        if mcb_stoch_guard:
            sk = features.get("stoch_k", 50.0)
            if mcb_stoch_guard == "skip_neutral" and 25.0 < sk < 75.0:
                return "skip"
            if mcb_stoch_guard == "require_extreme" and 15.0 < sk < 85.0:
                return "skip"
        mcb_vwap_guard = mutations.get("mcb_vwap_guard", "")
        if mcb_vwap_guard:
            vd = features.get("vwap_deviation", 0.0)
            if mcb_vwap_guard == "require_extended" and -0.001 < vd < 0.001:
                return "skip"
            if mcb_vwap_guard == "skip_extreme" and (vd > 0.003 or vd < -0.003):
                return "skip"
        mcb_obv_guard = mutations.get("mcb_obv_guard", "")
        if mcb_obv_guard == "require_aligned":
            obv_s = features.get("obv_slope", 0.0)
            if mcb_likely_dir == "up" and obv_s < 0.0:
                return "skip"
            if mcb_likely_dir == "down" and obv_s > 0.0:
                return "skip"
        bb_pct_b = features.get("bb_pct_b", 0.5)
        stoch_k_val = features.get("stoch_k", 50.0)
        vwap_dev = features.get("vwap_deviation", 0.0)
        obv_sl = features.get("obv_slope", 0.0)
        min_confirms = 4 if mcb_confirm_threshold == "high" else 3
        # Bullish multi-confirm: count independent oversold signals
        up_confirms = 0
        if close_location < 0.20:
            up_confirms += 1
        if rsi < 30.0:
            up_confirms += 1
        if bb_pct_b < 0.10:
            up_confirms += 1
        if stoch_k_val < 20.0:
            up_confirms += 1
        if vwap_dev < -0.001:
            up_confirms += 1
        if obv_sl > 0.05:
            up_confirms += 1
        if up_confirms >= min_confirms and direction_filter != "short_only":
            if mcb_wick_confirm != "on" or features.get("lower_wick_ratio", 0.0) > 0.25:
                return "up"
        # Bearish multi-confirm: count independent overbought signals
        dn_confirms = 0
        if close_location > 0.80:
            dn_confirms += 1
        if rsi > 70.0:
            dn_confirms += 1
        if bb_pct_b > 0.90:
            dn_confirms += 1
        if stoch_k_val > 80.0:
            dn_confirms += 1
        if vwap_dev > 0.001:
            dn_confirms += 1
        if obv_sl < -0.05:
            dn_confirms += 1
        if dn_confirms >= min_confirms and direction_filter != "long_only":
            if mcb_wick_confirm != "on" or features.get("upper_wick_ratio", 0.0) > 0.25:
                return "down"
        return "skip"

    if strategy_id == "vwap_reversion":
        # Mean reversion to VWAP: trade when price is significantly extended
        # from volume-weighted average price, with ATR confirming normal volatility.
        vr_regimes: set[str] = {"compression", "range", "event_driven"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            vr_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in vr_regimes:
            return "skip"
        if volume_context_guard == "thin_filter" and volume_ratio < 0.55:
            return "skip"
        if late_sample_guard == "on" and volatility > 0.0012:
            return "skip"
        if session_quality_filter == "skip_compression_toxic":
            if session_hour in {3, 5, 7, 8, 11, 13, 17, 20, 21, 23}:
                return "skip"
        # ── Forge indicator guards (universal) ──────
        vr_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "vr", vr_likely_dir):
            return "skip"
        # ── VR strategy-specific enrichment guards (P3) ──────
        vr_obv_guard = mutations.get("vr_obv_guard", "")
        if vr_obv_guard == "require_aligned":
            obv_s = features.get("obv_slope", 0.0)
            if vr_likely_dir == "up" and obv_s > 0.0:
                return "skip"  # reversion: OBV should diverge from price
            if vr_likely_dir == "down" and obv_s < 0.0:
                return "skip"
        vwap_dev = features.get("vwap_deviation", 0.0)
        atr_ratio_val = features.get("atr_ratio", 0.0)
        vr_dev_threshold = 0.002 if mutations.get("vr_deviation_threshold", "standard") == "standard" else 0.003
        vr_atr_cap = 0.02 if mutations.get("vr_atr_cap", "standard") == "standard" else 0.015
        # Skip if ATR is too high (volatile regime, VWAP unreliable)
        if atr_ratio_val > vr_atr_cap:
            return "skip"
        # Bullish: price significantly below VWAP, expect reversion up
        if vwap_dev < -vr_dev_threshold and rsi < 40.0:
            if direction_filter != "short_only":
                return "up"
        # Bearish: price significantly above VWAP, expect reversion down
        if vwap_dev > vr_dev_threshold and rsi > 60.0:
            if direction_filter != "long_only":
                return "down"
        return "skip"

    if strategy_id == "keltner_mean_reversion":
        # Mean reversion at Keltner Channel extremes in volatile regimes.
        # Keltner uses ATR (not std dev), better for non-normal distributions.
        km_regimes: set[str] = {"high_vol", "event_driven"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            km_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in km_regimes:
            return "skip"
        if volume_context_guard == "thin_filter" and volume_ratio < 0.55:
            return "skip"
        if session_quality_filter == "skip_compression_toxic":
            if session_hour in {3, 5, 7, 8, 11, 13, 17, 20, 21, 23}:
                return "skip"
        km_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "km", km_likely_dir):
            return "skip"
        kp = features.get("keltner_pos", 0.5)
        kw = features.get("keltner_width", 0.02)
        km_keltner_threshold = 0.10 if mutations.get("km_keltner_threshold", "standard") == "standard" else 0.05
        km_rsi_threshold = 35.0 if mutations.get("km_rsi_threshold", "standard") == "standard" else 25.0
        km_width_floor = 0.01 if mutations.get("km_width_floor", "standard") == "standard" else 0.015
        if kw < km_width_floor:
            return "skip"
        km_adx_confirm = mutations.get("km_adx_confirm", "off")
        if km_adx_confirm == "on":
            adx_val = features.get("adx_14", 0.0)
            if adx_val > 40.0:
                return "skip"
        # Bullish: price at lower Keltner extreme + RSI oversold
        if kp < km_keltner_threshold and rsi < km_rsi_threshold:
            if mutations.get("km_wick_confirm", "off") != "on" or features.get("lower_wick_ratio", 0.0) > 0.3:
                if direction_filter != "short_only":
                    return "up"
        # Bearish: price at upper Keltner extreme + RSI overbought
        if kp > (1.0 - km_keltner_threshold) and rsi > (100.0 - km_rsi_threshold):
            if mutations.get("km_wick_confirm", "off") != "on" or features.get("upper_wick_ratio", 0.0) > 0.3:
                if direction_filter != "long_only":
                    return "down"
        return "skip"

    if strategy_id == "volume_exhaustion_reversal":
        # Volume spikes at price extremes signal exhaustion — the move
        # has used up its fuel. Trade the reversal.
        ve_regimes: set[str] = {"event_driven", "high_vol"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            ve_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in ve_regimes:
            return "skip"
        if session_quality_filter == "skip_compression_toxic":
            if session_hour in {3, 5, 7, 8, 11, 13, 17, 20, 21, 23}:
                return "skip"
        ve_vol_floor = 2.0 if mutations.get("ve_volume_floor", "standard") == "standard" else 2.5
        ve_rsi = 30.0 if mutations.get("ve_rsi_threshold", "standard") == "standard" else 25.0
        ve_close_threshold = 0.15 if mutations.get("ve_close_threshold", "standard") == "standard" else 0.10
        ve_cmf_confirm = mutations.get("ve_cmf_confirm", "off")
        # Bullish exhaustion: huge volume + price hammered to lows + RSI oversold
        if volume_ratio > ve_vol_floor and close_location < ve_close_threshold and rsi < ve_rsi:
            if ve_cmf_confirm != "on" or features.get("cmf_20", 0.0) > -0.1:
                if direction_filter != "short_only":
                    return "up"
        # Bearish exhaustion: huge volume + price spiked to highs + RSI overbought
        if volume_ratio > ve_vol_floor and close_location > (1.0 - ve_close_threshold) and rsi > (100.0 - ve_rsi):
            if ve_cmf_confirm != "on" or features.get("cmf_20", 0.0) < 0.1:
                if direction_filter != "long_only":
                    return "down"
        return "skip"

    if strategy_id == "climax_reversal":
        # Larry Williams short-term exhaustion: require climax-style impulse
        # THEN a tight turn-window reclaim/rejection before taking reversal.
        # Differs from volume_exhaustion: adds timing structure + wick confirmation.
        cr2_regimes: set[str] = {"range", "event_driven", "high_vol"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            cr2_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in cr2_regimes:
            return "skip"
        if no_trade_window == "avoid_midmove_reversal_guessing":
            # Skip if move is extended but not climactic
            if abs(momentum) > 0.001 and volume_ratio < 1.5:
                return "skip"
        cr2_vol_floor = 1.8 if mutations.get("cr2_volume_floor", "standard") == "standard" else 2.2
        cr2_rsi_lo = 28.0 if mutations.get("cr2_rsi_threshold", "standard") == "standard" else 22.0
        cr2_rsi_hi = 72.0 if mutations.get("cr2_rsi_threshold", "standard") == "standard" else 78.0
        cr2_close_lo = 0.18 if mutations.get("cr2_close_threshold", "standard") == "standard" else 0.12
        # Session turn window: prefer session transitions (Larry Williams timing)
        cr2_session_turn = mutations.get("cr2_session_turn", "off")
        if cr2_session_turn == "on":
            # Tight turn windows at session boundaries (UTC hours)
            if session_hour not in {0, 8, 13, 16, 20}:
                return "skip"
        # Bullish climax reversal: price at extreme low + volume climax + RSI oversold
        if close_location < cr2_close_lo and volume_ratio > cr2_vol_floor and rsi < cr2_rsi_lo:
            # Require wick rejection (the "reclaim" part of Larry Williams timing)
            if reversal_confirmation in ("session_turn_reclaim", "base"):
                if lower_wick_ratio > 0.25:  # buyers stepped in
                    if direction_filter != "short_only":
                        return "up"
            elif reversal_confirmation == "reclaim_close":
                if lower_wick_ratio > 0.3 and reclaim_strength > 0.002:
                    if direction_filter != "short_only":
                        return "up"
        # Bearish climax reversal: price at extreme high + volume climax + RSI overbought
        if close_location > (1.0 - cr2_close_lo) and volume_ratio > cr2_vol_floor and rsi > cr2_rsi_hi:
            if reversal_confirmation in ("session_turn_reclaim", "base"):
                if upper_wick_ratio > 0.25:  # sellers stepped in
                    if direction_filter != "long_only":
                        return "down"
            elif reversal_confirmation == "reclaim_close":
                if upper_wick_ratio > 0.3 and reclaim_strength > 0.002:
                    if direction_filter != "long_only":
                        return "down"
        return "skip"

    if strategy_id == "intermarket_context_gate":
        # Murphy intermarket context: use wider-context trend + volatility as
        # proxy for cross-asset risk tone. Skip when local signal conflicts
        # with macro context (trend_2h diverges from signal direction).
        im_regimes: set[str] = {"event_driven", "high_vol", "compression"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            im_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in im_regimes:
            return "skip"
        if session_quality_filter == "skip_compression_toxic":
            if session_hour in {3, 5, 7, 8, 11, 13, 17, 20, 21, 23}:
                return "skip"
        # ── Forge indicator guards (universal) ──────
        im_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "im", im_likely_dir):
            return "skip"
        trend_2h = features.get("trend_2h", 0.0)
        pos_in_2h = features.get("pos_in_2h", 0.5)
        vol_2h = features.get("vol_2h", 0.0)
        # Cross-asset divergence proxy: if 2h trend is strong but current
        # price action disagrees, that's a "divergence" signal
        im_trend_threshold = 0.0003 if mutations.get("im_trend_strength", "standard") == "standard" else 0.0005
        im_divergence_mode = mutations.get("im_divergence_mode", "skip_conflict")
        # Bullish setup: oversold + RSI low
        if close_location < 0.20 and rsi < 35.0:
            # Check for macro conflict: bullish entry but 2h trend strongly bearish
            if im_divergence_mode == "skip_conflict" and trend_2h < -im_trend_threshold:
                return "skip"  # macro says down, don't fade
            if im_divergence_mode == "require_aligned" and trend_2h < 0:
                return "skip"  # require positive macro tone for UP entries
            if direction_filter != "short_only":
                return "up"
        # Bearish setup: overbought + RSI high
        if close_location > 0.80 and rsi > 65.0:
            if im_divergence_mode == "skip_conflict" and trend_2h > im_trend_threshold:
                return "skip"  # macro says up, don't fade
            if im_divergence_mode == "require_aligned" and trend_2h > 0:
                return "skip"  # require negative macro tone for DOWN entries
            if direction_filter != "long_only":
                return "down"
        return "skip"

    if strategy_id == "participation_gate_overlay":
        # Thorp/Van Tharp/Basso: risk-calibrated participation.
        # Uses feature-level proxies to detect "low-edge" conditions
        # and skips. This is a signal-level overlay, not position sizing.
        pg_regimes: set[str] = {"compression", "range", "event_driven", "trend", "high_vol"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            pg_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in pg_regimes:
            return "skip"
        # Edge quality proxies: skip when conditions suggest low-edge state
        pg_vol_regime = mutations.get("pg_volatility_regime", "skip_extreme")
        if pg_vol_regime == "skip_extreme":
            if volatility > 0.002 or range_width > 0.012:
                return "skip"  # too volatile = unreliable signals
        elif pg_vol_regime == "skip_dead":
            if volatility < 0.0002 and volume_ratio < 0.6:
                return "skip"  # dead market = no real signal
        # ── Forge indicator guards (universal) ──────
        pg_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "pg", pg_likely_dir):
            return "skip"
        # ── PG strategy-specific enrichment guards (P3) ──────
        pg_atr_guard = mutations.get("pg_atr_guard", "")
        if pg_atr_guard:
            atr_r = features.get("atr_ratio", 0.0)
            if pg_atr_guard == "skip_high_atr" and atr_r > 0.02:
                return "skip"
            if pg_atr_guard == "skip_very_high" and atr_r > 0.025:
                return "skip"
        pg_bb_guard = mutations.get("pg_bb_guard", "")
        if pg_bb_guard == "require_squeeze":
            bw = features.get("bb_width", 0.03)
            if bw > 0.02:
                return "skip"
        pg_macd_guard = mutations.get("pg_macd_guard", "")
        if pg_macd_guard == "skip_dead_macd":
            macd_h = features.get("macd_histogram", 0.0)
            if -0.00005 < macd_h < 0.00005:
                return "skip"
        pg_confidence_proxy = mutations.get("pg_confidence_proxy", "feature_agreement")
        if pg_confidence_proxy == "feature_agreement":
            # Require multiple features to agree (RSI + close_loc + momentum direction)
            bull_signals = 0
            bear_signals = 0
            if rsi < 35.0:
                bull_signals += 1
            if rsi > 65.0:
                bear_signals += 1
            if close_location < 0.25:
                bull_signals += 1
            if close_location > 0.75:
                bear_signals += 1
            if momentum < -0.0005:
                bull_signals += 1  # price falling = potential UP reversal
            if momentum > 0.0005:
                bear_signals += 1  # price rising = potential DOWN reversal
            # Only participate when 2+ signals agree
            if bull_signals >= 2 and direction_filter != "short_only":
                return "up"
            if bear_signals >= 2 and direction_filter != "long_only":
                return "down"
        elif pg_confidence_proxy == "extreme_only":
            # Only trade at absolute extremes (highest edge states)
            if close_location < 0.12 and rsi < 25.0:
                if direction_filter != "short_only":
                    return "up"
            if close_location > 0.88 and rsi > 75.0:
                if direction_filter != "long_only":
                    return "down"
        return "skip"

    # ══════════════════════════════════════════════════════════════════
    # SESSION 26: New quant-research strategy blocks
    # ══════════════════════════════════════════════════════════════════

    # ── momentum_zscore_reversal ───────────────────────────────────
    # Velocity-based signal: z-score of momentum captures rate-of-change
    # extremes, orthogonal to level-based RSI/close_location.
    # Targets trend + high_vol regimes (0 WF>=0.8 currently).
    if strategy_id == "momentum_zscore_reversal":
        mz_regimes = {"trend", "event_driven", "high_vol"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            mz_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in mz_regimes:
            return "skip"
        if session_quality_filter == "skip_compression_toxic" and session_code == 1.0:
            return "skip"
        mz_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "mz", mz_likely_dir):
            return "skip"
        mom_z = features.get("momentum_zscore", 0.0)
        ou_hl = features.get("ou_halflife", 100.0)
        mz_threshold_str = mutations.get("mz_zscore_threshold", "standard")
        mz_threshold = {"aggressive": 1.5, "standard": 2.0, "extreme": 2.5}.get(mz_threshold_str, 2.0)
        mz_rsi_confirm = mutations.get("mz_rsi_confirm", "on")
        mz_ou_gate = mutations.get("mz_ou_gate", "off")
        if mz_ou_gate == "on" and ou_hl > 15.0:
            return "skip"
        # Velocity extreme DOWN → price snap UP
        if mom_z < -mz_threshold:
            if mz_rsi_confirm == "on" and rsi > 35.0:
                return "skip"
            if direction_filter != "short_only":
                return "up"
        # Velocity extreme UP → price snap DOWN
        if mom_z > mz_threshold:
            if mz_rsi_confirm == "on" and rsi < 65.0:
                return "skip"
            if direction_filter != "long_only":
                return "down"
        return "skip"

    # ── linreg_deviation_reversion ─────────────────────────────────
    # Trend-aware mean reversion: revert to linear regression trend line,
    # not to static range. Fills the trend regime gap.
    if strategy_id == "linreg_deviation_reversion":
        lr_regimes = {"trend", "range"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            lr_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in lr_regimes:
            return "skip"
        if session_quality_filter == "skip_compression_toxic" and session_code == 1.0:
            return "skip"
        lr_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "lr", lr_likely_dir):
            return "skip"
        lr_dev = features.get("linreg_deviation", 0.0)
        trend_2h = features.get("trend_2h", 0.0)
        adx_val = features.get("adx_14", 0.0)
        lr_thresh_str = mutations.get("lr_deviation_threshold", "standard")
        lr_thresh = {"tight": 1.0, "standard": 1.5, "wide": 2.0}.get(lr_thresh_str, 1.5)
        lr_trend_confirm = mutations.get("lr_trend_confirm", "on")
        lr_adx_cap_str = mutations.get("lr_adx_cap", "standard")
        lr_adx_cap = {"tight": 30.0, "standard": 40.0}.get(lr_adx_cap_str, 40.0)
        if adx_val > lr_adx_cap:
            return "skip"
        # Below regression line → UP reversion
        if lr_dev < -lr_thresh:
            if lr_trend_confirm == "on" and trend_2h < -0.003:
                return "skip"  # don't revert against strong 2h downtrend
            if direction_filter != "short_only":
                return "up"
        # Above regression line → DOWN reversion
        if lr_dev > lr_thresh:
            if lr_trend_confirm == "on" and trend_2h > 0.003:
                return "skip"  # don't revert against strong 2h uptrend
            if direction_filter != "long_only":
                return "down"
        return "skip"

    # ── ou_adaptive_entry ──────────────────────────────────────────
    # Mathematical mean-reversion confirmation: only trade when
    # Ornstein-Uhlenbeck half-life confirms FAST reversion.
    if strategy_id == "ou_adaptive_entry":
        ou_regimes = {"compression", "range", "event_driven"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            ou_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in ou_regimes:
            return "skip"
        if session_quality_filter == "skip_compression_toxic" and session_code == 1.0:
            return "skip"
        ou_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "ou", ou_likely_dir):
            return "skip"
        ou_hl = features.get("ou_halflife", 100.0)
        hurst = features.get("hurst_exp", 0.5)
        entropy = features.get("shannon_entropy", 0.0)
        ou_cap_str = mutations.get("ou_halflife_cap", "standard")
        ou_cap = {"fast": 8.0, "standard": 12.0, "relaxed": 15.0}.get(ou_cap_str, 12.0)
        ou_hurst_gate = mutations.get("ou_hurst_gate", "off")
        ou_entropy_gate = mutations.get("ou_entropy_gate", "off")
        if ou_hl > ou_cap:
            return "skip"
        if ou_hurst_gate == "on" and hurst > 0.45:
            return "skip"  # not mean-reverting regime
        if ou_entropy_gate == "on" and entropy < 0.3:
            return "skip"  # too predictable/trending
        # Fast reversion + oversold → UP
        if close_location < 0.20 and rsi < 35.0:
            if direction_filter != "short_only":
                return "up"
        # Fast reversion + overbought → DOWN
        if close_location > 0.80 and rsi > 65.0:
            if direction_filter != "long_only":
                return "down"
        return "skip"

    # ── macd_histogram_reversal ────────────────────────────────────
    # MACD histogram is #2 ML feature importance but barely used as
    # primary signal. Combined with OBV divergence = accumulation
    # detection during sell-off.
    if strategy_id == "macd_histogram_reversal":
        mh_regimes = {"compression", "range", "event_driven", "trend", "high_vol"}
        extend_regimes = mutations.get("extend_regimes", "")
        if extend_regimes:
            mh_regimes = {r.strip() for r in extend_regimes.split(",") if r.strip()}
        if detected_regime not in mh_regimes:
            return "skip"
        if session_quality_filter == "skip_compression_toxic" and session_code == 1.0:
            return "skip"
        mh_likely_dir = "up" if close_location < 0.5 else "down"
        if _apply_indicator_guards(mutations, features, "mh", mh_likely_dir):
            return "skip"
        macd_h = features.get("macd_histogram", 0.0)
        obv_sl = features.get("obv_slope", 0.0)
        mom_z = features.get("momentum_zscore", 0.0)
        vol_ratio = features.get("volume_ratio", 1.0)
        mh_macd_str = mutations.get("mh_macd_threshold", "standard")
        mh_macd_thresh = {"standard": 0.001, "deep": 0.002}.get(mh_macd_str, 0.001)
        mh_obv_diverge = mutations.get("mh_obv_diverge", "off")
        mh_momentum_gate = mutations.get("mh_momentum_gate", "off")
        if vol_ratio < 0.8:
            return "skip"  # too quiet
        # Bearish MACD + selling pressure → potential UP reversal
        if macd_h < -mh_macd_thresh:
            if mh_momentum_gate == "on" and mom_z > -1.5:
                return "skip"
            if mh_obv_diverge == "on" and obv_sl < 0.0:
                return "skip"  # OBV also falling = no accumulation
            if direction_filter != "short_only":
                return "up"
        # Bullish MACD + buying pressure → potential DOWN reversal
        if macd_h > mh_macd_thresh:
            if mh_momentum_gate == "on" and mom_z < 1.5:
                return "skip"
            if mh_obv_diverge == "on" and obv_sl > 0.0:
                return "skip"  # OBV also rising = no distribution
            if direction_filter != "long_only":
                return "down"
        return "skip"

    return "skip"


def _trade_return(prediction: str, actual: str, fee_penalty: float) -> float:
    if prediction == "skip":
        return 0.0
    gross = 1.0 if prediction == actual else -1.0
    return gross - fee_penalty


def _gross_trade_return(prediction: str, actual: str) -> float:
    if prediction == "skip":
        return 0.0
    return 1.0 if prediction == actual else -1.0


def _regime_stats(stats: dict[str, dict[str, float | int]]) -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    for regime, values in stats.items():
        trades = int(values.get("trade_count", 0) or 0)
        wins = int(values.get("win_count", 0) or 0)
        pnl_total = float(values.get("pnl_total", 0.0) or 0.0)
        result[regime] = {
            "trade_count": trades,
            "win_rate": round(wins / trades, 4) if trades else 0.0,
            "avg_return": round(pnl_total / trades, 4) if trades else 0.0,
        }
    return result


def _segment_stats(segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for item in segments:
        gross_returns = item.get("gross_returns", [])
        gross_returns = gross_returns if isinstance(gross_returns, list) else []
        trade_count = len(gross_returns)
        net_returns = [float(value) - 0.04 for value in gross_returns]
        profitability_score = round(_profitability(net_returns), 4) if net_returns else 0.0
        result.append(
            {
                "segment_id": item.get("segment_id"),
                "start_contract_id": item.get("start_contract_id"),
                "end_contract_id": item.get("end_contract_id"),
                "trade_count": trade_count,
                "profitability_score": profitability_score,
                "win_rate": round(sum(1 for value in gross_returns if float(value) > 0.0) / trade_count, 4) if trade_count else 0.0,
                "avg_return": round(sum(net_returns) / trade_count, 4) if trade_count else 0.0,
                "trade_count_gate_pass": trade_count >= int(item.get("minimum_trade_count", 0) or 0),
            }
        )
    return result


def _stress_stats(gross_returns: list[float], minimum_trade_count: int) -> dict[str, dict[str, float | int | bool]]:
    scenarios = {
        "base": 0.04,
        "elevated_fees": 0.08,
        "fee_and_slippage": 0.12,
    }
    result: dict[str, dict[str, float | int | bool]] = {}
    trade_count = len(gross_returns)
    for label, penalty in scenarios.items():
        net_returns = [float(value) - penalty for value in gross_returns]
        result[label] = {
            "trade_count": trade_count,
            "profitability_score": round(_profitability(net_returns), 4) if net_returns else 0.0,
            "avg_return": round(sum(net_returns) / trade_count, 4) if trade_count else 0.0,
            "trade_count_gate_pass": trade_count >= minimum_trade_count,
        }
    return result


def _equity_drawdown(returns: list[float]) -> float:
    equity = 0.0
    peak = 0.0
    worst = 0.0
    for item in returns:
        equity += item
        peak = max(peak, equity)
        worst = min(worst, equity - peak)
    if peak <= 0.0 and worst < 0.0:
        return min(0.99, abs(worst) / max(1.0, abs(worst)))
    if peak <= 0.0:
        return 0.0
    return min(0.99, abs(worst) / peak)


def _profitability(returns: list[float]) -> float:
    if not returns:
        return 0.0
    avg = mean(returns)
    scaled = 0.5 + avg / 2.0
    return max(0.0, min(0.99, scaled))


def _sharpe(returns: list[float]) -> float:
    active = [item for item in returns if item != 0.0]
    if len(active) < 2:
        return 0.0
    sigma = pstdev(active)
    if sigma == 0.0:
        return 0.0
    return round(mean(active) / sigma * math.sqrt(len(active)), 4)


def _paper_trade_readiness(profitability_score: float, sharpe_ratio: float, max_drawdown: float, coverage_ratio: float, holdout_profitability: float) -> float:
    raw = profitability_score * 0.35 + min(1.2, sharpe_ratio) * 0.18 + coverage_ratio * 0.17 + holdout_profitability * 0.2 - max_drawdown * 0.35
    return round(max(0.0, min(0.99, raw)), 4)


def data_paths(runtime_root: Path, asset: str = "btc", timeframe: str = "15m") -> tuple[Path, Path]:
    slug = asset.lower()
    candles = runtime_root / "data" / f"{slug}_1m_candles.jsonl"
    contracts = runtime_root / "data" / f"{slug}_up_down_{timeframe}_contracts.jsonl"
    if candles.exists() and contracts.exists():
        return candles, contracts
    return runtime_root / "data" / f"sample_{slug}_1m_candles.jsonl", runtime_root / "data" / f"sample_{slug}_up_down_{timeframe}_contracts.jsonl"


def _exact_data_paths(runtime_root: Path, asset: str, timeframe: str) -> tuple[Path, Path] | None:
    slug = asset.lower()
    candles = runtime_root / "data" / f"{slug}_1m_candles.jsonl"
    contracts = runtime_root / "data" / f"{slug}_up_down_{timeframe}_contracts.jsonl"
    if candles.exists() and contracts.exists():
        return candles, contracts
    return None


def _ordered_assets(raw_asset_universe: str) -> list[str]:
    requested = [item.strip().lower() for item in raw_asset_universe.split(",") if item.strip()]
    ordered: list[str] = []
    for asset in requested + list(SUPPORTED_BACKTEST_ASSETS):
        if asset and asset not in ordered:
            ordered.append(asset)
    return ordered or ["btc"]


def _ordered_timeframes(requested_timeframe: str) -> list[str]:
    ordered: list[str] = []
    requested = requested_timeframe.strip() or "15m"
    for timeframe in (requested,) + SUPPORTED_BACKTEST_TIMEFRAMES:
        if timeframe and timeframe not in ordered:
            ordered.append(timeframe)
    return ordered


def _resolve_backtest_data(runtime_root: Path, raw_asset_universe: str, requested_timeframe: str) -> dict[str, Any] | None:
    requested_assets = _ordered_assets(raw_asset_universe)
    requested_asset = requested_assets[0]
    for asset in requested_assets:
        for timeframe in _ordered_timeframes(requested_timeframe):
            resolved = _exact_data_paths(runtime_root, asset, timeframe)
            if resolved is None:
                continue
            fallback_notes: list[str] = []
            if asset != requested_asset:
                fallback_notes.append(f"requested asset `{requested_asset.upper()}` unavailable")
            if timeframe != requested_timeframe:
                fallback_notes.append(f"requested timeframe `{requested_timeframe}` unavailable")
            return {
                "asset": asset,
                "timeframe": timeframe,
                "candle_path": resolved[0],
                "contract_path": resolved[1],
                "requested_asset": requested_asset,
                "requested_timeframe": requested_timeframe,
                "fallback_reason": "; ".join(fallback_notes),
            }
    return None


def paper_trade_data_paths(runtime_root: Path, asset: str = "btc", timeframe: str = "15m") -> tuple[Path | None, Path | None]:
    slug = asset.lower()
    candles = runtime_root / "data" / f"paper_trade_{slug}_1m_candles.jsonl"
    contracts = runtime_root / "data" / f"paper_trade_{slug}_up_down_{timeframe}_contracts.jsonl"
    if candles.exists() and contracts.exists():
        return candles, contracts
    return None, None


def run_backtest(mutations: dict[str, str], runtime_root: Path, contract_limit: int | None = None, guard_fn=None) -> dict[str, Any] | None:
    raw_asset_universe = str(mutations.get("asset_universe", "BTC")).strip() or "BTC"
    requested_timeframe = str(mutations.get("timeframe", "15m")).strip() or "15m"
    resolved_data = _resolve_backtest_data(runtime_root, raw_asset_universe, requested_timeframe)
    if resolved_data is None:
        return None
    candle_path = Path(resolved_data["candle_path"])
    contract_path = Path(resolved_data["contract_path"])
    candles = _candles(candle_path)
    contracts = _contracts(contract_path)
    if not candles or not contracts:
        return None
    # Staged evaluation support: limit contracts for quick/medium screening
    if contract_limit is not None and contract_limit > 0:
        contracts = contracts[:contract_limit]
    candle_times = [item.ts.timestamp() for item in candles]

    returns: list[float] = []
    active_returns: list[float] = []
    active_gross_returns: list[float] = []
    holdout_returns: list[float] = []
    holdout_active_returns: list[float] = []
    trade_count = 0
    coverage_count = 0
    predictions: list[str] = []
    actuals: list[str] = []
    regime_trade_stats: dict[str, dict[str, float | int]] = {}
    holdout_start = max(1, int(len(contracts) * 0.8))
    fee_penalty = 0.04
    minimum_trade_count = max(25, int(len(contracts) * 0.02))
    desired_regime = mutations.get("market_regime", "")
    split_count = 5
    segment_size = max(1, len(contracts) // split_count)
    walk_forward_buckets: list[dict[str, Any]] = []
    for segment_index in range(split_count):
        start = segment_index * segment_size
        if start >= len(contracts):
            break
        end = len(contracts) if segment_index == split_count - 1 else min(len(contracts), (segment_index + 1) * segment_size)
        walk_forward_buckets.append(
            {
                "segment_id": f"wf-{segment_index + 1}",
                "start_contract_id": contracts[start].contract_id,
                "end_contract_id": contracts[end - 1].contract_id,
                "gross_returns": [],
                "minimum_trade_count": max(5, int(max(1, end - start) * 0.02)),
                "regime_eligible_count": 0,
            }
        )
    regime_eligible_total = 0
    for index, contract in enumerate(contracts):
        lookback = _window_candles(candles, candle_times, contract)
        if len(lookback) < 5:
            continue
        coverage_count += 1
        features = _feature_row(lookback, contract)
        features.update(_wider_context(candles, candle_times, contract))
        detected_regime = _detected_regime(features)
        if desired_regime and detected_regime == desired_regime:
            seg_idx = min(len(walk_forward_buckets) - 1, index // segment_size)
            walk_forward_buckets[seg_idx]["regime_eligible_count"] += 1
            regime_eligible_total += 1
        prediction = _signal(mutations, features)
        if guard_fn is not None and prediction != "skip":
            prediction = guard_fn(features, prediction)
        actual = contract.settlement_direction
        gross_trade_return = _gross_trade_return(prediction, actual)
        trade_return = _trade_return(prediction, actual, fee_penalty)
        returns.append(trade_return)
        if prediction != "skip":
            trade_count += 1
            predictions.append(prediction)
            actuals.append(actual)
            active_returns.append(trade_return)
            active_gross_returns.append(gross_trade_return)
            bucket = regime_trade_stats.setdefault(detected_regime, {"trade_count": 0, "win_count": 0, "pnl_total": 0.0})
            bucket["trade_count"] = int(bucket["trade_count"]) + 1
            bucket["win_count"] = int(bucket["win_count"]) + (1 if prediction == actual else 0)
            bucket["pnl_total"] = float(bucket["pnl_total"]) + trade_return
            segment_index = min(len(walk_forward_buckets) - 1, index // segment_size)
            walk_forward_buckets[segment_index]["gross_returns"].append(gross_trade_return)
        if index >= holdout_start:
            holdout_returns.append(trade_return)
            if prediction != "skip":
                holdout_active_returns.append(trade_return)
    if desired_regime and regime_eligible_total > 0:
        minimum_trade_count = max(25, int(regime_eligible_total * 0.02))
        for wfb in walk_forward_buckets:
            rec = int(wfb.get("regime_eligible_count", 0))
            if rec > 0:
                wfb["minimum_trade_count"] = max(5, int(rec * 0.02))

    if coverage_count == 0:
        return None
    win_rate = 0.0
    if predictions:
        wins = sum(1 for prediction, actual in zip(predictions, actuals) if prediction == actual)
        win_rate = round(wins / len(predictions), 4)
    profitability_score = round(_profitability(active_returns), 4)
    sharpe_ratio = _sharpe(active_returns)
    max_drawdown = round(_equity_drawdown(active_returns), 4) if active_returns else 0.0
    coverage_ratio = round(coverage_count / len(contracts), 4)
    holdout_profitability = round(_profitability(holdout_active_returns), 4) if holdout_active_returns else profitability_score
    walk_forward_stats = _segment_stats(walk_forward_buckets)
    walk_forward_passes = sum(1 for item in walk_forward_stats if bool(item.get("trade_count_gate_pass")) and float(item.get("profitability_score", 0.0) or 0.0) >= 0.5)
    walk_forward_consistency = round(walk_forward_passes / len(walk_forward_stats), 4) if walk_forward_stats else 0.0
    stress_stats = _stress_stats(active_gross_returns, minimum_trade_count)
    # Stress resilience measures fee sensitivity, not sample size.
    # Trade count gating is enforced separately in the verdict logic.
    # A strategy with 163 trades and PS > 0.5 under all fee scenarios IS stress resilient.
    stress_min_trades = max(15, minimum_trade_count // 4)
    stress_passes = sum(
        1
        for item in stress_stats.values()
        if int(item.get("trade_count", 0) or 0) >= stress_min_trades and float(item.get("profitability_score", 0.0) or 0.0) >= 0.5
    )
    stress_resilience = round(stress_passes / len(stress_stats), 4) if stress_stats else 0.0
    base_stress_profitability = float(stress_stats.get("base", {}).get("profitability_score", profitability_score) or profitability_score)
    paper_trade_readiness = round(
        max(
            0.0,
            min(
                0.99,
                _paper_trade_readiness(base_stress_profitability, sharpe_ratio, max_drawdown, coverage_ratio, holdout_profitability)
                + walk_forward_consistency * 0.12
                + stress_resilience * 0.08,
            ),
        ),
        4,
    )
    trade_count_gate_pass = trade_count >= minimum_trade_count
    effective_contract_pool = regime_eligible_total if (desired_regime and regime_eligible_total > 0) else len(contracts)
    verdict = (
        "approve"
        if (
            paper_trade_readiness >= 0.78
            and max_drawdown <= 0.2
            and trade_count >= max(minimum_trade_count, int(effective_contract_pool * 0.025))
            and walk_forward_consistency >= 0.8
            and stress_resilience >= 0.66
        )
        else "defer"
        if profitability_score >= 0.55 and trade_count_gate_pass and walk_forward_consistency >= 0.4
        else "reject"
    )
    next_step = "queue_for_paper_trade" if verdict == "approve" else "hold_for_more_backtest_evidence" if verdict == "defer" else "run_contradiction_probe"
    evaluated_asset = str(resolved_data["asset"]).upper()
    evaluated_timeframe = str(resolved_data["timeframe"])
    fallback_reason = str(resolved_data.get("fallback_reason", "")).strip()
    lesson = f"Backtested on {trade_count} active {evaluated_asset} {evaluated_timeframe} contract decisions across {coverage_count} covered windows."
    if fallback_reason:
        lesson += f" Fallback used because {fallback_reason}."
    return {
        "profitability_score": profitability_score,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "win_rate": win_rate,
        "paper_trade_readiness": paper_trade_readiness,
        "verdict_confidence": round(max(0.0, min(0.99, 0.45 + profitability_score * 0.25 + win_rate * 0.15 + coverage_ratio * 0.15 - max_drawdown * 0.1)), 4),
        "verdict": verdict,
        "recommended_next_step": next_step,
        "lesson": lesson,
        "boundary": "Insufficient heavy-backtest breadth or unstable returns still block promotion." if verdict != "approve" else "Promotion allowed only for outer paper-trade validation.",
        "contract_count": len(contracts),
        "covered_contract_count": coverage_count,
        "trade_count": trade_count,
        "minimum_trade_count": minimum_trade_count,
        "trade_count_gate_pass": trade_count_gate_pass,
        "holdout_profitability_score": holdout_profitability,
        "walk_forward_consistency": walk_forward_consistency,
        "walk_forward_stats": walk_forward_stats,
        "stress_resilience": stress_resilience,
        "stress_stats": stress_stats,
        "regime_stats": _regime_stats(regime_trade_stats),
        "data_mode": "contract_window_backtest",
        "requested_asset_universe": raw_asset_universe,
        "requested_timeframe": requested_timeframe,
        "evaluated_asset": evaluated_asset,
        "evaluated_timeframe": evaluated_timeframe,
        "data_fallback_reason": fallback_reason,
        "candle_path": str(candle_path),
        "contract_path": str(contract_path),
    }


def _evaluate_asset_paper_trade(
    mutations: dict[str, str],
    candle_path: Path,
    contract_path: Path,
    asset: str,
    max_contracts: int,
    guard_fn=None,
) -> tuple[list[dict[str, Any]], int]:
    """Evaluate paper trade signals for a single asset. Returns (decision_rows, coverage_count)."""
    candles = _candles(candle_path)
    contracts = _contracts(contract_path)
    if not candles or not contracts:
        return [], 0
    candle_times = [item.ts.timestamp() for item in candles]
    selected = contracts[-max(1, max_contracts):]
    rows: list[dict[str, Any]] = []
    coverage = 0
    fee_penalty = 0.04
    for contract in selected:
        lookback = _window_candles(candles, candle_times, contract)
        if len(lookback) < 5:
            continue
        coverage += 1
        features = _feature_row(lookback, contract)
        features.update(_wider_context(candles, candle_times, contract))
        detected_regime = _detected_regime(features)
        prediction = _signal(mutations, features)
        if guard_fn is not None and prediction != "skip":
            prediction = guard_fn(features, prediction)
        actual = contract.settlement_direction
        trade_return = _trade_return(prediction, actual, fee_penalty)
        rows.append({
            "contract_id": contract.contract_id,
            "asset": asset,
            "open_ts": contract.open_ts.isoformat().replace("+00:00", "Z"),
            "close_ts": contract.close_ts.isoformat().replace("+00:00", "Z"),
            "prediction": prediction,
            "actual": actual,
            "detected_regime": detected_regime,
            "correct": prediction == actual if prediction != "skip" else None,
            "realized_return": round(trade_return, 4),
        })
    return rows, coverage


def run_paper_trade_validation(mutations: dict[str, str], runtime_root: Path, *, max_contracts: int = 96, guard_fn=None) -> dict[str, Any]:
    raw_universe = str(mutations.get("asset_universe", "BTC"))
    assets = [a.strip().lower() for a in raw_universe.split(",") if a.strip()]
    if not assets:
        assets = ["btc"]
    timeframe = str(mutations.get("timeframe", "15m")).strip() or "15m"

    all_decisions: list[dict[str, Any]] = []
    total_coverage = 0
    total_selected = 0
    any_data = False

    for asset in assets:
        candle_path, contract_path = paper_trade_data_paths(runtime_root, asset=asset, timeframe=timeframe)
        if candle_path is None or contract_path is None:
            continue
        rows, coverage = _evaluate_asset_paper_trade(mutations, candle_path, contract_path, asset, max_contracts, guard_fn=guard_fn)
        if rows:
            any_data = True
            all_decisions.extend(rows)
            total_coverage += coverage

    if not any_data:
        # Fallback: try BTC with default timeframe
        candle_path, contract_path = paper_trade_data_paths(runtime_root)
        if candle_path is not None and contract_path is not None:
            rows, coverage = _evaluate_asset_paper_trade(mutations, candle_path, contract_path, "btc", max_contracts, guard_fn=guard_fn)
            if rows:
                any_data = True
                all_decisions.extend(rows)
                total_coverage += coverage

    if not any_data:
        return {
            "status": "pending_data",
            "paper_trade_recommendation": "await_shadow_contract_feed",
            "sample_contract_count": 0,
            "trade_count": 0,
            "win_rate": 0.0,
            "profitability_score": 0.0,
            "max_drawdown": 0.0,
            "boundary": "Paper-trade dataset is missing.",
        }

    # Sort decisions chronologically across all assets
    all_decisions.sort(key=lambda r: r.get("open_ts", ""))

    active_returns = [r["realized_return"] for r in all_decisions if r["prediction"] != "skip"]
    predictions = [r["prediction"] for r in all_decisions if r["prediction"] != "skip"]
    actuals = [r["actual"] for r in all_decisions if r["prediction"] != "skip"]

    trade_count = len(predictions)
    win_rate = round(sum(1 for p, a in zip(predictions, actuals) if p == a) / trade_count, 4) if trade_count else 0.0
    profitability_score = round(_profitability(active_returns), 4) if active_returns else 0.0
    max_drawdown = round(_equity_drawdown(active_returns), 4) if active_returns else 0.0
    sharpe_ratio = _sharpe(active_returns) if active_returns else 0.0

    # Per-regime diagnostic stats
    regime_stats: dict[str, dict[str, Any]] = {}
    for row in all_decisions:
        if row.get("prediction") == "skip":
            continue
        regime = row.get("detected_regime", "unknown")
        bucket = regime_stats.setdefault(regime, {"trades": 0, "wins": 0, "returns": []})
        bucket["trades"] += 1
        if row.get("correct"):
            bucket["wins"] += 1
        bucket["returns"].append(row.get("realized_return", 0.0))
    regime_summary = {}
    for regime, bucket in regime_stats.items():
        regime_summary[regime] = {
            "trades": bucket["trades"],
            "win_rate": round(bucket["wins"] / max(1, bucket["trades"]), 4),
            "avg_return": round(mean(bucket["returns"]), 4) if bucket["returns"] else 0.0,
        }

    # Paper-trade recommendation with statistical minimum for demotion.
    _dd_ref_n = 500
    _dd_base = 0.22
    dd_gate = min(0.8, _dd_base * (_dd_ref_n / max(1, trade_count)) ** 0.5) if trade_count > 0 else _dd_base
    paper_trade_recommendation = (
        "advance_toward_live_readiness"
        if profitability_score >= 0.53 and win_rate >= 0.53 and max_drawdown <= dd_gate and trade_count >= 20
        else "collect_more_paper_data"
        if trade_count < 30 or (profitability_score >= 0.48 and win_rate >= 0.45)
        else "demote_to_benchmark"
    )
    boundary = (
        "Paper-trade slice supports live-readiness review."
        if paper_trade_recommendation == "advance_toward_live_readiness"
        else "Paper-trade slice is still thin or unstable; do not treat it as live-ready."
        if paper_trade_recommendation == "collect_more_paper_data"
        else "Paper-trade slice failed to confirm the bridge candidate."
    )

    first_id = all_decisions[0]["contract_id"] if all_decisions else ""
    last_id = all_decisions[-1]["contract_id"] if all_decisions else ""
    assets_evaluated = sorted(set(r.get("asset", "btc") for r in all_decisions))

    return {
        "status": "executed",
        "paper_trade_recommendation": paper_trade_recommendation,
        "sample_contract_count": len(all_decisions),
        "covered_contract_count": total_coverage,
        "trade_count": trade_count,
        "win_rate": win_rate,
        "profitability_score": profitability_score,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "regime_stats": regime_summary,
        "assets_evaluated": assets_evaluated,
        "start_contract_id": first_id,
        "end_contract_id": last_id,
        "boundary": boundary,
        "decisions": all_decisions,
    }
