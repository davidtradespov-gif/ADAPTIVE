from __future__ import annotations

import json
import math
import sys
import gc
from dataclasses import asdict, dataclass
from datetime import UTC
from pathlib import Path
from zoneinfo import ZoneInfo


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_PYTHON_PACKAGES = REPO_ROOT / ".python_packages"
if str(LOCAL_PYTHON_PACKAGES) not in sys.path:
    sys.path.insert(0, str(LOCAL_PYTHON_PACKAGES))

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


DATASET_ROOT = REPO_ROOT / "mgc_comex_trades_package (2)" / "mgc_comex_trades_package" / "trades_s3_mgc_parquet"
REPORTS_DIR = REPO_ROOT / "reports"
JSON_REPORT = REPORTS_DIR / "strategy_01_absorption_reversal_report.json"
MARKDOWN_REPORT = REPORTS_DIR / "strategy_01_absorption_reversal_report.md"
NEW_YORK_TZ = ZoneInfo("America/New_York")
MGC_TICK_SIZE = 0.10
MGC_TICK_VALUE = 1.00
MODEL_FEATURES = [
    "size_zscore",
    "rolling_signed_flow",
    "cvd_delta_short",
    "price_delta_short",
    "pressure_efficiency",
    "close_location",
    "rejection_strength",
    "sweep_distance",
    "opening_range_bonus",
    "direction_code",
    "minutes_from_open",
    "session_code",
]


@dataclass(frozen=True)
class SessionConfig:
    key: str
    label: str
    code: int
    start_hour: int
    end_hour: int
    opening_range_minutes: int = 30


@dataclass(frozen=True)
class RunnerVariant:
    name: str
    runner_trail_distance_ticks: int
    add_on_activation_ticks: int | None = None
    add_on_contracts: int = 0
    add_on_min_score: float = 0.78


SESSION_LIBRARY = {
    "asia": SessionConfig(key="asia", label="Asia", code=0, start_hour=20, end_hour=1, opening_range_minutes=45),
    "london": SessionConfig(key="london", label="London", code=1, start_hour=2, end_hour=8, opening_range_minutes=30),
    "new_york": SessionConfig(key="new_york", label="New York", code=2, start_hour=8, end_hour=13, opening_range_minutes=30),
}


@dataclass
class StrategyConfig:
    train_last_n_days: int = 180
    session_names: tuple[str, ...] = ("asia", "london", "new_york")
    trade_target_candidates: tuple[int, ...] = (40,)
    rolling_window_trades: int = 10
    short_flow_window: int = 4
    price_window: int = 4
    zscore_threshold: float = 0.35
    signed_flow_threshold: float = 0.0
    absorption_efficiency_cap: float = 1.10
    min_sweep_ticks: int = 0
    reclaim_ticks: int = 0
    rejection_seconds: int = 15
    cooldown_seconds: int = 8
    hard_stop_ticks: int = 5
    break_even_activation_ticks: int = 3
    break_even_lock_ticks: int = 1
    trail_activation_ticks: int = 4
    trail_distance_ticks: int = 3
    runner_min_score: float = 0.72
    runner_activation_ticks: int = 6
    runner_trail_distance_ticks: int = 9
    runner_variants: tuple[RunnerVariant, ...] = (
        RunnerVariant(name="base_runner_9", runner_trail_distance_ticks=9),
        RunnerVariant(name="breathing_runner_15", runner_trail_distance_ticks=15),
        RunnerVariant(name="addon_12_trail_15", runner_trail_distance_ticks=15, add_on_activation_ticks=12, add_on_contracts=1),
    )
    normal_max_hold_seconds: int = 900
    runner_max_hold_seconds: int = 3600
    opposite_flow_exit_threshold: float = 50.0
    adverse_ticks_before_flow_exit: int = 3
    min_rejection_close_location: float = 0.55
    max_rejection_close_location: float = 0.45
    min_probability_score: float = 0.0
    daily_trade_buffer: int = 60
    daily_loss_limit_dollars: float = 1_000_000.0
    starting_balance: float = 10_000.0
    max_drawdown_fraction: float = 0.20
    target_risk_fraction_floor: float = 0.05
    target_risk_fraction_cap: float = 0.10
    commission_per_side: float = 0.85
    slippage_per_side_ticks: int = 1


def resolved_sessions(cfg: StrategyConfig) -> list[SessionConfig]:
    return [SESSION_LIBRARY[name] for name in cfg.session_names]


def load_day(path: Path) -> pd.DataFrame:
    parts = sorted(path.glob("*.parquet"))
    if not parts:
        return pd.DataFrame()
    needed_columns = ["ticker", "timestamp", "price", "size"]
    df = pd.concat([pd.read_parquet(p, columns=needed_columns) for p in parts], ignore_index=True)
    if df.empty:
        return df
    df["ts_utc"] = pd.to_datetime(df["timestamp"], unit="ns", utc=True)
    df["ts_ny"] = df["ts_utc"].dt.tz_convert(NEW_YORK_TZ)
    df["is_spread"] = df["ticker"].astype(str).str.contains("-", regex=False)
    return df


def available_day_dirs() -> list[Path]:
    days = []
    for day in sorted(p for p in DATASET_ROOT.iterdir() if p.is_dir()):
        if any(day.glob("*.parquet")):
            days.append(day)
    return days


def select_last_n_available_days(n: int) -> tuple[str, str, list[str]]:
    days = available_day_dirs()
    selected = days[-n:] if len(days) > n else days
    selected_names = [p.name.split("=", 1)[1] for p in selected]
    return selected_names[0], selected_names[-1], selected_names


def session_hour_mask(hours: pd.Series, session: SessionConfig) -> pd.Series:
    if session.start_hour < session.end_hour:
        return (hours >= session.start_hour) & (hours < session.end_hour)
    return (hours >= session.start_hour) | (hours < session.end_hour)


def filter_session(df: pd.DataFrame, session: SessionConfig) -> pd.DataFrame:
    if df.empty:
        return df
    hours = df["ts_ny"].dt.hour
    result = df[session_hour_mask(hours, session)].copy()
    result = result[~result["is_spread"]].copy()
    return result


def aggregate_session(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    work = df.sort_values("ts_utc").copy()
    work["ts_utc_sec"] = work["ts_utc"].dt.floor("s")
    work["ts_ny_sec"] = work["ts_ny"].dt.floor("s")
    work["price_change"] = work["price"].diff()
    work["signed_size"] = work["size"] * work["price_change"].fillna(0.0).apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    grouped = (
        work.groupby("ts_utc_sec", as_index=False)
        .agg(
            ts_ny=("ts_ny_sec", "last"),
            price=("price", "last"),
            high=("price", "max"),
            low=("price", "min"),
            volume=("size", "sum"),
            trades=("size", "count"),
            signed_flow=("signed_size", "sum"),
            ticker=("ticker", "last"),
        )
    )
    grouped["ts_utc"] = grouped["ts_utc_sec"]
    return grouped


def build_features(df: pd.DataFrame, cfg: StrategyConfig, session: SessionConfig) -> pd.DataFrame:
    if df.empty:
        return df
    result = df.copy()
    session_start = result["ts_ny"].iloc[0]
    opening_range_end = session_start + pd.Timedelta(minutes=session.opening_range_minutes)
    rolling_min_periods = max(3, min(20, cfg.rolling_window_trades))
    result["price_change"] = result["price"].diff()
    result["price_range"] = result["high"] - result["low"]
    result["bar_return"] = result["price"].diff().fillna(0.0)
    result["rolling_signed_flow"] = result["signed_flow"].rolling(cfg.rolling_window_trades, min_periods=rolling_min_periods).sum()
    result["cvd_delta_short"] = result["signed_flow"].rolling(cfg.short_flow_window, min_periods=3).sum()
    result["price_delta_short"] = result["price"].diff(cfg.price_window).fillna(0.0)
    result["rolling_size_mean"] = result["volume"].rolling(cfg.rolling_window_trades, min_periods=rolling_min_periods).mean()
    result["rolling_size_std"] = result["volume"].rolling(cfg.rolling_window_trades, min_periods=rolling_min_periods).std()
    result["size_zscore"] = (
        (result["volume"] - result["rolling_size_mean"]) /
        result["rolling_size_std"].replace(0, pd.NA)
    ).fillna(0.0)
    result["rolling_high"] = result["high"].rolling(cfg.rolling_window_trades, min_periods=rolling_min_periods).max().shift(1)
    result["rolling_low"] = result["low"].rolling(cfg.rolling_window_trades, min_periods=rolling_min_periods).min().shift(1)
    result["cum_vwap_num"] = (result["price"] * result["volume"]).cumsum()
    result["cum_vwap_den"] = result["volume"].cumsum().replace(0, pd.NA)
    result["session_vwap"] = (result["cum_vwap_num"] / result["cum_vwap_den"]).ffill()
    opening_mask = result["ts_ny"] <= opening_range_end
    if opening_mask.any():
        opening_high = float(result.loc[opening_mask, "high"].max())
        opening_low = float(result.loc[opening_mask, "low"].min())
    else:
        opening_high = float(result["high"].iloc[0])
        opening_low = float(result["low"].iloc[0])
    result["opening_range_high"] = opening_high
    result["opening_range_low"] = opening_low
    result["distance_from_vwap"] = result["price"] - result["session_vwap"]
    result["absorption_efficiency"] = (
        result["price_range"] / result["volume"].replace(0, pd.NA)
    ).fillna(0.0)
    result["pressure_efficiency"] = (
        result["price_delta_short"].abs() /
        result["cvd_delta_short"].abs().replace(0, pd.NA)
    ).fillna(0.0)
    result["close_location"] = (
        (result["price"] - result["low"]) /
        result["price_range"].replace(0, pd.NA)
    ).fillna(0.5)
    result["minutes_from_open"] = (result["ts_ny"] - session_start).dt.total_seconds() / 60.0
    result["session_code"] = session.code
    result["session_name"] = session.label
    return result


def find_events(df: pd.DataFrame, cfg: StrategyConfig, session: SessionConfig, trade_date: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    candidates = []
    for i in range(cfg.rolling_window_trades, len(df) - 5):
        row = df.iloc[i]
        if row["size_zscore"] < cfg.zscore_threshold:
            continue
        if abs(float(row["rolling_signed_flow"])) < cfg.signed_flow_threshold:
            continue
        if float(row["absorption_efficiency"]) > cfg.absorption_efficiency_cap:
            continue
        prior_high = row["rolling_high"]
        prior_low = row["rolling_low"]
        if pd.isna(prior_high) or pd.isna(prior_low):
            continue
        prior_high = float(prior_high)
        prior_low = float(prior_low)
        opening_high = float(row["opening_range_high"])
        opening_low = float(row["opening_range_low"])
        high = float(row["high"])
        low = float(row["low"])
        price = float(row["price"])
        close_location = float(row["close_location"])
        cvd_delta_short = float(row["cvd_delta_short"])
        price_delta_short = float(row["price_delta_short"])
        pressure_efficiency = float(row["pressure_efficiency"])
        short_anchor = prior_high
        long_anchor = prior_low
        short_sweep = high >= short_anchor + cfg.min_sweep_ticks
        long_sweep = low <= long_anchor - cfg.min_sweep_ticks
        short_pressure_ok = cvd_delta_short > 0 and pressure_efficiency <= 0.55
        long_pressure_ok = cvd_delta_short < 0 and pressure_efficiency <= 0.55
        if (
            short_sweep
            and price <= short_anchor - cfg.reclaim_ticks
            and short_pressure_ok
            and close_location <= cfg.max_rejection_close_location
        ):
            direction = "short"
            anchor = short_anchor
            sweep_price = high
        elif (
            long_sweep
            and price >= long_anchor + cfg.reclaim_ticks
            and long_pressure_ok
            and close_location >= cfg.min_rejection_close_location
        ):
            direction = "long"
            anchor = long_anchor
            sweep_price = low
        else:
            continue
        if direction == "short":
            rejection_strength = 1.0 - close_location
            sweep_distance = max(0.0, sweep_price - anchor)
            opposite_pressure = max(0.0, price_delta_short)
        else:
            rejection_strength = close_location
            sweep_distance = max(0.0, anchor - sweep_price)
            opposite_pressure = max(0.0, -price_delta_short)
        opening_range_bonus = 1.0 if (direction == "short" and sweep_price >= opening_high) or (direction == "long" and sweep_price <= opening_low) else 0.0
        score = (
            min(2.5, float(row["size_zscore"])) * 0.20 +
            min(3.0, abs(cvd_delta_short) / 80.0) * 0.20 +
            min(1.0, rejection_strength) * 0.25 +
            min(2.0, sweep_distance / 2.0) * 0.10 +
            min(2.0, max(0.0, 0.55 - pressure_efficiency) / 0.25) * 0.10 +
            min(1.5, max(0.0, 2.0 - opposite_pressure)) * 0.05 +
            opening_range_bonus * 0.10
        )
        probability_score = 1.0 / (1.0 + math.exp(-(score - 1.25)))
        if probability_score < cfg.min_probability_score:
            continue
        candidates.append({
            "trade_date": trade_date,
            "event_ts_utc": row["ts_utc"].isoformat(),
            "event_ts_ny": row["ts_ny"].isoformat(),
            "event_calendar_date": row["ts_ny"].date().isoformat(),
            "session_name": session.label,
            "session_code": session.code,
            "direction": direction,
            "ticker": row["ticker"],
            "anchor_price": anchor,
            "event_price": price,
            "sweep_price": sweep_price,
            "entry_price": price,
            "size": int(row["volume"]),
            "size_zscore": float(row["size_zscore"]),
            "rolling_signed_flow": float(row["rolling_signed_flow"]),
            "cvd_delta_short": cvd_delta_short,
            "price_delta_short": price_delta_short,
            "pressure_efficiency": pressure_efficiency,
            "close_location": close_location,
            "rejection_strength": rejection_strength,
            "sweep_distance": sweep_distance,
            "opening_range_bonus": opening_range_bonus,
            "direction_code": -1 if direction == "short" else 1,
            "minutes_from_open": float(row["minutes_from_open"]),
            "probability_score": probability_score,
            "session_vwap": float(row["session_vwap"]),
        })
    return pd.DataFrame(candidates)


def trade_pnl(direction: str, exit_price: float, entries: list[float], round_trip_cost: float) -> float:
    pnl = 0.0
    for entry_price in entries:
        price_delta = (exit_price - entry_price) if direction == "long" else (entry_price - exit_price)
        pnl_ticks = price_delta / MGC_TICK_SIZE
        pnl += pnl_ticks * MGC_TICK_VALUE - round_trip_cost
    return pnl


def mtm_pnl(direction: str, mark_price: float, entries: list[float], round_trip_cost: float) -> float:
    return trade_pnl(direction, mark_price, entries, round_trip_cost)


def per_contract_risk_dollars(cfg: StrategyConfig) -> float:
    stop_risk = cfg.hard_stop_ticks * MGC_TICK_VALUE
    round_trip_cost = 2 * cfg.commission_per_side + 2 * cfg.slippage_per_side_ticks * MGC_TICK_VALUE
    return stop_risk + round_trip_cost


def simulate_trades(
    events: pd.DataFrame,
    full_df: pd.DataFrame,
    cfg: StrategyConfig,
    runner_variant: RunnerVariant | None = None,
) -> pd.DataFrame:
    if events.empty:
        return pd.DataFrame()
    trades = []
    round_trip_cost = 2 * cfg.commission_per_side + 2 * cfg.slippage_per_side_ticks * MGC_TICK_VALUE
    full_df = full_df.sort_values("ts_utc").reset_index(drop=True)
    session_end_ts = full_df["ts_utc"].iloc[-1]
    ts_values = full_df["ts_utc"].astype("int64").to_numpy()
    prices = full_df["price"].astype(float).to_numpy()
    signed_flows = full_df["signed_flow"].astype(float).to_numpy()
    for _, event in events.iterrows():
        entry_ts = pd.Timestamp(event["event_ts_utc"])
        entry_price = float(event["entry_price"])
        direction = event["direction"]
        runner_candidate = float(event.get("probability_score", 0.0)) >= cfg.runner_min_score
        runner_trail_distance_ticks = (
            runner_variant.runner_trail_distance_ticks if runner_variant else cfg.runner_trail_distance_ticks
        )
        add_on_activation_ticks = runner_variant.add_on_activation_ticks if runner_variant else None
        add_on_contracts = runner_variant.add_on_contracts if runner_variant else 0
        add_on_min_score = runner_variant.add_on_min_score if runner_variant else 1.0
        add_on_allowed = (
            runner_candidate
            and add_on_activation_ticks is not None
            and add_on_contracts > 0
            and float(event.get("probability_score", 0.0)) >= add_on_min_score
        )
        max_hold_seconds = cfg.runner_max_hold_seconds if runner_candidate else cfg.normal_max_hold_seconds
        max_exit_ts = min(session_end_ts, entry_ts + pd.Timedelta(seconds=max_hold_seconds))
        start_idx = ts_values.searchsorted(entry_ts.value, side="right")
        end_idx = ts_values.searchsorted(max_exit_ts.value, side="right")
        if start_idx >= end_idx:
            continue
        reached_session_end = max_exit_ts == session_end_ts
        exit_reason = "session_flat" if reached_session_end else "time"
        exit_price = float(prices[end_idx - 1])
        exit_ts = pd.Timestamp(ts_values[end_idx - 1], tz=UTC)
        best_price = entry_price
        stop_distance = cfg.hard_stop_ticks * MGC_TICK_SIZE
        stop_price = entry_price - stop_distance if direction == "long" else entry_price + stop_distance
        trail_active = False
        runner_active = False
        entries = [entry_price]
        add_on_count = 0
        for row_idx in range(start_idx, end_idx):
            price = float(prices[row_idx])
            signed_flow = float(signed_flows[row_idx])
            if direction == "long":
                best_price = max(best_price, price)
                favorable_ticks = (best_price - entry_price) / MGC_TICK_SIZE
                if favorable_ticks >= cfg.break_even_activation_ticks:
                    stop_price = max(stop_price, entry_price + cfg.break_even_lock_ticks * MGC_TICK_SIZE)
                if favorable_ticks >= cfg.trail_activation_ticks:
                    trail_active = True
                if runner_candidate and favorable_ticks >= cfg.runner_activation_ticks:
                    runner_active = True
                if add_on_allowed and add_on_count < add_on_contracts and favorable_ticks >= add_on_activation_ticks:
                    entries.append(price)
                    add_on_count += 1
                if trail_active:
                    trail_distance = runner_trail_distance_ticks if runner_active else cfg.trail_distance_ticks
                    stop_price = max(stop_price, best_price - trail_distance * MGC_TICK_SIZE)
                if price <= stop_price:
                    exit_price = stop_price
                    exit_ts = pd.Timestamp(ts_values[row_idx], tz=UTC)
                    exit_reason = "trailing_stop" if trail_active else "hard_stop"
                    break
                if (
                    price <= entry_price - cfg.adverse_ticks_before_flow_exit * MGC_TICK_SIZE
                    and signed_flow <= -cfg.opposite_flow_exit_threshold
                ):
                    exit_price = price
                    exit_ts = pd.Timestamp(ts_values[row_idx], tz=UTC)
                    exit_reason = "opposite_flow"
                    break
            else:
                best_price = min(best_price, price)
                favorable_ticks = (entry_price - best_price) / MGC_TICK_SIZE
                if favorable_ticks >= cfg.break_even_activation_ticks:
                    stop_price = min(stop_price, entry_price - cfg.break_even_lock_ticks * MGC_TICK_SIZE)
                if favorable_ticks >= cfg.trail_activation_ticks:
                    trail_active = True
                if runner_candidate and favorable_ticks >= cfg.runner_activation_ticks:
                    runner_active = True
                if add_on_allowed and add_on_count < add_on_contracts and favorable_ticks >= add_on_activation_ticks:
                    entries.append(price)
                    add_on_count += 1
                if trail_active:
                    trail_distance = runner_trail_distance_ticks if runner_active else cfg.trail_distance_ticks
                    stop_price = min(stop_price, best_price + trail_distance * MGC_TICK_SIZE)
                if price >= stop_price:
                    exit_price = stop_price
                    exit_ts = pd.Timestamp(ts_values[row_idx], tz=UTC)
                    exit_reason = "trailing_stop" if trail_active else "hard_stop"
                    break
                if (
                    price >= entry_price + cfg.adverse_ticks_before_flow_exit * MGC_TICK_SIZE
                    and signed_flow >= cfg.opposite_flow_exit_threshold
                ):
                    exit_price = price
                    exit_ts = pd.Timestamp(ts_values[row_idx], tz=UTC)
                    exit_reason = "opposite_flow"
                    break
        pnl_dollars = trade_pnl(direction, exit_price, entries, round_trip_cost)
        trades.append({
            "trade_date": event["trade_date"],
            "event_ts_utc": event["event_ts_utc"],
            "direction": direction,
            "ticker": event["ticker"],
            "session_name": event["session_name"],
            "session_code": event["session_code"],
            "entry_price": entry_price,
            "exit_price": exit_price,
            "exit_ts_utc": exit_ts.isoformat(),
            "exit_reason": exit_reason,
            "runner_candidate": runner_candidate,
            "runner_active": runner_active,
            "add_on_count": add_on_count,
            "position_units": len(entries),
            "entry_prices": list(entries),
            "pnl_dollars_1_contract": pnl_dollars,
        })
    return pd.DataFrame(trades)


def fit_probability_model(events: pd.DataFrame, trades: pd.DataFrame) -> pd.DataFrame:
    if events.empty or trades.empty:
        return events
    labels = trades[["event_ts_utc", "direction", "ticker", "session_name", "pnl_dollars_1_contract"]].copy()
    labels["target_hit"] = labels["pnl_dollars_1_contract"].gt(2.0).astype(int)
    merged = events.merge(labels, on=["event_ts_utc", "direction", "ticker", "session_name"], how="left")
    merged["target_hit"] = merged["target_hit"].fillna(0).astype(int)
    if merged["target_hit"].nunique() < 2:
        return merged
    x = merged[MODEL_FEATURES].fillna(0.0)
    y = merged["target_hit"]
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000)),
        ]
    )
    model.fit(x, y)
    merged["probability_score"] = model.predict_proba(x)[:, 1]
    return merged


def build_candidate_pool(selected_days: list[str], cfg: StrategyConfig) -> dict:
    total_raw_rows = 0
    total_session_rows = 0
    event_frames: list[pd.DataFrame] = []
    trade_frames: list[pd.DataFrame] = []
    session_row_counts = {session.label: 0 for session in resolved_sessions(cfg)}
    session_event_counts = {session.label: 0 for session in resolved_sessions(cfg)}
    for day_name in selected_days:
        day_path = DATASET_ROOT / f"date={day_name}"
        raw = load_day(day_path)
        if raw.empty:
            continue
        total_raw_rows += len(raw)
        for session in resolved_sessions(cfg):
            session_df = filter_session(raw, session)
            if session_df.empty:
                continue
            aggregated = aggregate_session(session_df)
            if aggregated.empty:
                continue
            total_session_rows += len(aggregated)
            session_row_counts[session.label] += len(aggregated)
            features = build_features(aggregated, cfg, session)
            events = find_events(features, cfg, session, trade_date=day_name)
            if events.empty:
                continue
            session_event_counts[session.label] += len(events)
            trades = simulate_trades(events, aggregated, cfg)
            event_frames.append(events)
            if not trades.empty:
                trade_frames.append(trades)
            del session_df, aggregated, features, events, trades
            gc.collect()
        del raw
        gc.collect()
    all_events = pd.concat(event_frames, ignore_index=True) if event_frames else pd.DataFrame()
    all_trades = pd.concat(trade_frames, ignore_index=True) if trade_frames else pd.DataFrame()
    candidate_pool_count = int(len(all_events))
    scored_events = fit_probability_model(all_events, all_trades)
    del all_events, all_trades
    gc.collect()
    return {
        "start": selected_days[0] if selected_days else None,
        "end": selected_days[-1] if selected_days else None,
        "selected_days": selected_days,
        "selected_day_count": len(selected_days),
        "raw_rows": int(total_raw_rows),
        "session_rows": int(total_session_rows),
        "session_row_counts": session_row_counts,
        "session_event_counts": session_event_counts,
        "scored_events": scored_events,
        "candidate_pool": candidate_pool_count,
    }


def select_top_candidates(events: pd.DataFrame, cfg: StrategyConfig, daily_trade_target: int) -> pd.DataFrame:
    if events.empty:
        return events
    selected_frames: list[pd.DataFrame] = []
    for _, day_events in events.groupby("trade_date"):
        ranked = day_events.sort_values(
            by=["probability_score", "rejection_strength", "size_zscore"],
            ascending=[False, False, False],
        ).reset_index(drop=True)
        kept = []
        kept_ts: list[pd.Timestamp] = []
        for _, row in ranked.iterrows():
            event_ts = pd.Timestamp(row["event_ts_utc"])
            too_close = any(abs((event_ts - prior_ts).total_seconds()) < cfg.cooldown_seconds for prior_ts in kept_ts)
            if too_close:
                continue
            kept.append(row.to_dict())
            kept_ts.append(event_ts)
            if len(kept) >= daily_trade_target + cfg.daily_trade_buffer:
                break
        if kept:
            kept_df = pd.DataFrame(kept).sort_values("event_ts_utc").reset_index(drop=True)
            selected_frames.append(kept_df.head(daily_trade_target))
    if not selected_frames:
        return pd.DataFrame()
    return pd.concat(selected_frames, ignore_index=True)


def compute_intrabar_drawdown(realized_trades: pd.DataFrame, cfg: StrategyConfig) -> dict:
    if realized_trades.empty:
        return {
            "intrabar_max_drawdown_dollars": 0.0,
            "intrabar_max_drawdown_fraction": 0.0,
        }
    round_trip_cost = 2 * cfg.commission_per_side + 2 * cfg.slippage_per_side_ticks * MGC_TICK_VALUE
    sessions_by_label = {session.label: session for session in resolved_sessions(cfg)}
    equity_events: dict[int, list[float]] = {}
    for (trade_date, session_name), trades in realized_trades.groupby(["trade_date", "session_name"]):
        day_path = DATASET_ROOT / f"date={trade_date}"
        raw = load_day(day_path)
        session = sessions_by_label.get(session_name)
        if raw.empty or session is None:
            continue
        bars = aggregate_session(filter_session(raw, session)).sort_values("ts_utc").reset_index(drop=True)
        if bars.empty:
            continue
        ts_values = bars["ts_utc"].astype("int64").to_numpy()
        prices = bars["price"].astype(float).to_numpy()
        for _, trade in trades.iterrows():
            entry_ts = pd.Timestamp(trade["event_ts_utc"])
            exit_ts = pd.Timestamp(trade["exit_ts_utc"])
            start_idx = ts_values.searchsorted(entry_ts.value, side="right")
            end_idx = ts_values.searchsorted(exit_ts.value, side="right")
            if start_idx >= end_idx:
                continue
            entries = list(trade["entry_prices"]) if isinstance(trade["entry_prices"], list) else [float(trade["entry_price"])]
            contracts = int(trade["contracts"])
            prior_open = 0.0
            for row_idx in range(start_idx, end_idx):
                ts_key = int(ts_values[row_idx])
                open_pnl = mtm_pnl(str(trade["direction"]), float(prices[row_idx]), entries, round_trip_cost) * contracts
                delta = open_pnl - prior_open
                event = equity_events.setdefault(ts_key, [0.0, 0.0])
                event[0] += delta
                prior_open = open_pnl
            exit_key = int(ts_values[end_idx - 1])
            exit_event = equity_events.setdefault(exit_key, [0.0, 0.0])
            exit_event[1] += float(trade["pnl_dollars"])
            exit_event[0] -= prior_open
        del raw, bars
        gc.collect()
    equity = cfg.starting_balance
    peak = equity
    max_dd = 0.0
    open_total = 0.0
    for _, (open_delta, realized_delta) in sorted(equity_events.items()):
        open_total += open_delta
        equity += realized_delta
        mark_to_market_equity = equity + open_total
        peak = max(peak, mark_to_market_equity)
        max_dd = max(max_dd, peak - mark_to_market_equity)
    return {
        "intrabar_max_drawdown_dollars": max_dd,
        "intrabar_max_drawdown_fraction": max_dd / cfg.starting_balance,
    }


def apply_dynamic_sizing(trades: pd.DataFrame, cfg: StrategyConfig, daily_trade_target: int, selected_day_count: int) -> dict:
    if trades.empty:
        return {
            "trades": 0,
            "ending_balance": cfg.starting_balance,
            "max_drawdown_dollars": 0.0,
            "max_drawdown_fraction": 0.0,
            "intrabar_max_drawdown_dollars": 0.0,
            "intrabar_max_drawdown_fraction": 0.0,
            "avg_trades_per_day": 0.0,
            "net_pnl": 0.0,
            "contracts_cap": 0,
            "win_rate": 0.0,
            "avg_trade_pnl": 0.0,
            "baseline_max_drawdown_1_contract": 0.0,
            "selected_trade_target": daily_trade_target,
            "annualized_run_rate": 0.0,
        }
    baseline_equity = cfg.starting_balance
    baseline_peak = baseline_equity
    baseline_max_dd = 0.0
    for _, row in trades.iterrows():
        baseline_equity += row["pnl_dollars_1_contract"]
        baseline_peak = max(baseline_peak, baseline_equity)
        baseline_max_dd = max(baseline_max_dd, baseline_peak - baseline_equity)
    drawdown_budget = cfg.starting_balance * cfg.max_drawdown_fraction
    contracts_cap = max(1, math.floor(drawdown_budget / max(baseline_max_dd, per_contract_risk_dollars(cfg))))

    balance = cfg.starting_balance
    equity_peak = balance
    max_dd = 0.0
    trade_dates: dict[str, int] = {}
    realized = []
    current_day = None
    daily_realized_pnl = 0.0
    day_locked = False
    for _, row in trades.sort_values("event_ts_utc").iterrows():
        trade_date = row["trade_date"]
        if current_day != trade_date:
            current_day = trade_date
            daily_realized_pnl = 0.0
            day_locked = False
        if day_locked:
            continue
        trade_dates[trade_date] = trade_dates.get(trade_date, 0) + 1
        contract_risk = per_contract_risk_dollars(cfg)
        max_contracts = max(1, math.floor((balance * cfg.target_risk_fraction_cap) / contract_risk))
        min_contracts = max(1, math.floor((balance * cfg.target_risk_fraction_floor) / contract_risk))
        contracts = min(contracts_cap, max(1, min(max_contracts, max(min_contracts, 1))))
        pnl = row["pnl_dollars_1_contract"] * contracts
        balance += pnl
        daily_realized_pnl += pnl
        equity_peak = max(equity_peak, balance)
        drawdown = equity_peak - balance
        max_dd = max(max_dd, drawdown)
        realized.append({
            **row.to_dict(),
            "contracts": contracts,
            "pnl_dollars": pnl,
            "balance_after": balance,
        })
        if daily_realized_pnl <= -cfg.daily_loss_limit_dollars:
            day_locked = True
    avg_trades_per_day = sum(trade_dates.values()) / max(1, len(trade_dates))
    pnl_values = [trade["pnl_dollars"] for trade in realized]
    net_pnl = balance - cfg.starting_balance
    annualized_run_rate = net_pnl * 252 / max(1, selected_day_count)
    realized_df = pd.DataFrame(realized)
    intrabar = compute_intrabar_drawdown(realized_df, cfg)
    return {
        "trades": len(realized),
        "ending_balance": balance,
        "max_drawdown_dollars": max_dd,
        "max_drawdown_fraction": max_dd / cfg.starting_balance,
        "intrabar_max_drawdown_dollars": intrabar["intrabar_max_drawdown_dollars"],
        "intrabar_max_drawdown_fraction": intrabar["intrabar_max_drawdown_fraction"],
        "avg_trades_per_day": avg_trades_per_day,
        "net_pnl": net_pnl,
        "baseline_max_drawdown_1_contract": baseline_max_dd,
        "contracts_cap": contracts_cap,
        "win_rate": (sum(1 for value in pnl_values if value > 0) / len(pnl_values)) if pnl_values else 0.0,
        "avg_trade_pnl": (sum(pnl_values) / len(pnl_values)) if pnl_values else 0.0,
        "selected_trade_target": daily_trade_target,
        "annualized_run_rate": annualized_run_rate,
        "trade_details": realized[:25],
    }


def session_counts(df: pd.DataFrame, column: str) -> dict[str, int]:
    if df.empty or column not in df.columns:
        return {}
    grouped = df[column].value_counts().sort_index()
    return {str(name): int(value) for name, value in grouped.items()}


def simulate_selected_events(
    selected_events: pd.DataFrame,
    pool: dict,
    cfg: StrategyConfig,
    runner_variant: RunnerVariant | None = None,
) -> pd.DataFrame:
    if selected_events.empty:
        return pd.DataFrame()
    trade_frames: list[pd.DataFrame] = []
    sessions_by_label = {session.label: session for session in resolved_sessions(cfg)}
    for (trade_date, session_name), events in selected_events.groupby(["trade_date", "session_name"]):
        day_path = DATASET_ROOT / f"date={trade_date}"
        raw = load_day(day_path)
        session = sessions_by_label.get(session_name)
        if raw.empty or session is None:
            continue
        bars = aggregate_session(filter_session(raw, session))
        if bars.empty:
            continue
        trades = simulate_trades(events, bars, cfg, runner_variant=runner_variant)
        if not trades.empty:
            trade_frames.append(trades)
        del raw, bars, trades
        gc.collect()
    if not trade_frames:
        return pd.DataFrame()
    result = pd.concat(trade_frames, ignore_index=True).sort_values("event_ts_utc").reset_index(drop=True)
    del trade_frames
    gc.collect()
    return result


def evaluate_variant(
    pool: dict,
    cfg: StrategyConfig,
    daily_trade_target: int,
    runner_variant: RunnerVariant | None = None,
) -> dict:
    selected_events = select_top_candidates(pool["scored_events"], cfg, daily_trade_target)
    selected_trades = simulate_selected_events(selected_events, pool, cfg, runner_variant=runner_variant)
    summary = apply_dynamic_sizing(selected_trades, cfg, daily_trade_target, pool["selected_day_count"])
    return {
        "runner_variant": asdict(runner_variant) if runner_variant else None,
        "trade_target": daily_trade_target,
        "events": int(len(selected_events)),
        "trades": int(len(selected_trades)),
        "runner_trades": int(selected_trades["runner_candidate"].sum()) if "runner_candidate" in selected_trades else 0,
        "runner_active_trades": int(selected_trades["runner_active"].sum()) if "runner_active" in selected_trades else 0,
        "add_on_trades": int((selected_trades["add_on_count"] > 0).sum()) if "add_on_count" in selected_trades else 0,
        "total_add_on_units": int(selected_trades["add_on_count"].sum()) if "add_on_count" in selected_trades else 0,
        "selected_session_counts": session_counts(selected_events, "session_name"),
        "selected_trades_by_session": session_counts(selected_trades, "session_name"),
        "summary": summary,
    }


def variant_sort_key(variant: dict, cfg: StrategyConfig) -> tuple[int, int, float, float, float]:
    summary = variant["summary"]
    in_trade_band = 1 if 25.0 <= summary["avg_trades_per_day"] <= 50.0 else 0
    within_drawdown = 1 if summary["max_drawdown_fraction"] <= cfg.max_drawdown_fraction else 0
    return (
        within_drawdown,
        in_trade_band,
        summary["net_pnl"],
        -summary["max_drawdown_fraction"],
        summary["avg_trades_per_day"],
    )


def build_search_results(pool: dict, cfg: StrategyConfig) -> tuple[list[dict], dict]:
    variants = [
        evaluate_variant(pool, cfg, target, runner_variant=runner_variant)
        for target in cfg.trade_target_candidates
        for runner_variant in cfg.runner_variants
    ]
    ranked = sorted(variants, key=lambda variant: variant_sort_key(variant, cfg), reverse=True)
    return ranked, ranked[0]


def compact_summary(summary: dict, include_trade_details: bool = False) -> dict:
    result = {key: value for key, value in summary.items() if key != "trade_details"}
    if include_trade_details:
        result["trade_details"] = summary.get("trade_details", [])
    return result


def write_markdown(report: dict) -> str:
    sessions = ", ".join(session["label"] for session in report["sessions"])
    best = report["best_variant"]
    summary = best["summary"]
    lines = [
        "# Strategy 01 Absorption Reversal Report",
        "",
        "## Scope",
        "",
        "- Instrument: `MGC`",
        f"- Sessions: `{sessions}`",
        "- Setup family: absorption reversal / failed continuation",
        "- Account context: `10,000` sim",
        "- Strategy target band: `25` to `50` trades per day with max `20%` drawdown",
        "",
        "## Important Honesty Note",
        "",
        "This report uses the segmented MGC dataset currently available in the repository. It is not a claim of a continuous recent six-month train plus one-year OOS sample.",
        "The probability selector is still fit on the same candidate pool used to rank opportunities in this run, so this remains a strategy-construction result rather than a true validation result.",
        "",
        "## V2 Search Outcome",
        "",
        f"- Selected trade target: `{best['trade_target']}` per day",
        f"- Runner variant: `{best['runner_variant']['name']}`",
        f"- Average realized trades per day: `{summary['avg_trades_per_day']:.2f}`",
        f"- Net PnL: `${summary['net_pnl']:.2f}`",
        f"- Max drawdown fraction: `{summary['max_drawdown_fraction']:.4f}`",
        f"- Annualized run-rate from this training window: `${summary['annualized_run_rate']:.2f}`",
        f"- Runner-qualified trades: `{best['runner_trades']}`",
        f"- Runner-active trades: `{best['runner_active_trades']}`",
        f"- Add-on trades: `{best['add_on_trades']}`",
        "",
        "## Candidate Search Grid",
        "",
    ]
    for variant in report["search_results"]:
        variant_summary = variant["summary"]
        variant_name = variant["runner_variant"]["name"]
        lines.append(
            f"- Target `{variant['trade_target']}`, variant `{variant_name}`: trades/day `{variant_summary['avg_trades_per_day']:.2f}`, "
            f"net `${variant_summary['net_pnl']:.2f}`, drawdown `{variant_summary['max_drawdown_fraction']:.4f}`, "
            f"annualized `${variant_summary['annualized_run_rate']:.2f}`, add-on trades `{variant['add_on_trades']}`"
        )
    lines.extend([
        "",
        "## Train Window",
        "",
        f"- Date range: `{report['pool']['start']}` -> `{report['pool']['end']}`",
        f"- Selected available day folders: `{report['pool']['selected_day_count']}`",
        f"- Raw rows: `{report['pool']['raw_rows']}`",
        f"- Aggregated session rows across all modeled sessions: `{report['pool']['session_rows']}`",
        f"- Raw candidate pool: `{report['pool']['candidate_pool']}`",
        f"- Selected event candidates: `{best['events']}`",
        f"- Simulated trades: `{best['trades']}`",
        f"- Win rate: `{summary['win_rate']:.4f}`",
        f"- Average trade PnL: `${summary['avg_trade_pnl']:.2f}`",
        f"- Baseline max drawdown at 1 contract: `${summary['baseline_max_drawdown_1_contract']:.2f}`",
        f"- Dynamic contracts cap from {report['config']['max_drawdown_fraction']:.0%} drawdown budget: `{summary['contracts_cap']}`",
        f"- Ending balance: `${summary['ending_balance']:.2f}`",
        f"- Max drawdown dollars: `${summary['max_drawdown_dollars']:.2f}`",
        "",
        "## Session Mix",
        "",
    ])
    for session_label, count in sorted(best["selected_session_counts"].items()):
        lines.append(f"- Selected events from `{session_label}`: `{count}`")
    for session_label, count in sorted(best["selected_trades_by_session"].items()):
        lines.append(f"- Realized trades from `{session_label}`: `{count}`")
    lines.extend([
        "",
        "## Notes",
        "",
        "- V2 keeps the same strategy family and extends it across Asia, London, and New York rather than inventing a new unrelated setup.",
        "- Daily selection is now global across all modeled sessions, which narrows the focus to the strongest same-day opportunities instead of forcing equal participation from each session.",
        "- The annualized figure above is only a training-window run-rate projection from segmented history, not a validated yearly claim.",
        "- The next honest step is to freeze this V2 configuration and test it on a later chronological validation block before making any live-quality performance claim.",
        "",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    cfg = StrategyConfig()
    REPORTS_DIR.mkdir(exist_ok=True)
    _, _, selected_days = select_last_n_available_days(cfg.train_last_n_days)
    pool = build_candidate_pool(selected_days, cfg)
    search_results, best_variant = build_search_results(pool, cfg)
    report = {
        "generated_at_utc": pd.Timestamp.now(tz=UTC).isoformat(),
        "config": asdict(cfg),
        "sessions": [asdict(session) for session in resolved_sessions(cfg)],
        "pool": {
            "start": pool["start"],
            "end": pool["end"],
            "selected_day_count": pool["selected_day_count"],
            "raw_rows": pool["raw_rows"],
            "session_rows": pool["session_rows"],
            "candidate_pool": pool["candidate_pool"],
            "session_row_counts": pool["session_row_counts"],
            "session_event_counts": pool["session_event_counts"],
        },
        "search_results": [
            {
                "runner_variant": variant["runner_variant"],
                "trade_target": variant["trade_target"],
                "events": variant["events"],
                "trades": variant["trades"],
                "runner_trades": variant["runner_trades"],
                "runner_active_trades": variant["runner_active_trades"],
                "add_on_trades": variant["add_on_trades"],
                "total_add_on_units": variant["total_add_on_units"],
                "selected_session_counts": variant["selected_session_counts"],
                "selected_trades_by_session": variant["selected_trades_by_session"],
                "summary": compact_summary(variant["summary"]),
            }
            for variant in search_results
        ],
        "best_variant": {
            "runner_variant": best_variant["runner_variant"],
            "trade_target": best_variant["trade_target"],
            "events": best_variant["events"],
            "trades": best_variant["trades"],
            "runner_trades": best_variant["runner_trades"],
            "runner_active_trades": best_variant["runner_active_trades"],
            "add_on_trades": best_variant["add_on_trades"],
            "total_add_on_units": best_variant["total_add_on_units"],
            "selected_session_counts": best_variant["selected_session_counts"],
            "selected_trades_by_session": best_variant["selected_trades_by_session"],
            "summary": compact_summary(best_variant["summary"], include_trade_details=True),
        },
    }
    JSON_REPORT.write_text(json.dumps(report, indent=2))
    MARKDOWN_REPORT.write_text(write_markdown(report))
    print(f"Wrote {JSON_REPORT}")
    print(f"Wrote {MARKDOWN_REPORT}")


if __name__ == "__main__":
    main()
