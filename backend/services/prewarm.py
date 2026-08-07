"""Warm analytics caches on startup so the API stays responsive under load."""

from __future__ import annotations

import logging
import threading
import time
from typing import Any

from position_families import DEFAULT_POSITION_FAMILY

_log = logging.getLogger("pass_scout.prewarm")

_lock = threading.Lock()
_state: dict[str, Any] = {
    "ready": False,
    "loading": False,
    "started_at": None,
    "finished_at": None,
    "error": None,
    "steps": [],
}


def prewarm_status() -> dict[str, Any]:
    with _lock:
        return dict(_state)


def is_ready() -> bool:
    with _lock:
        return bool(_state["ready"])


def _mark_step(label: str) -> None:
    with _lock:
        _state["steps"].append(label)
    _log.info("Prewarm: %s", label)


def _run_prewarm() -> None:
    family = DEFAULT_POSITION_FAMILY
    t0 = time.perf_counter()

    from services.data_parts import get_data_parts
    from services.maps_service import load_aggregated_maps, load_xp_passes_grouped
    from services.similarity_service import _cached_pools

    _mark_step("player_pool")
    get_data_parts(family)

    _mark_step("similarity_pools")
    _cached_pools()

    _mark_step("xp_passes_grouped")
    load_xp_passes_grouped(family)

    _mark_step("aggregated_maps")
    load_aggregated_maps(250, family)

    elapsed = time.perf_counter() - t0
    with _lock:
        _state["ready"] = True
        _state["loading"] = False
        _state["finished_at"] = time.time()
        _state["elapsed_s"] = round(elapsed, 1)
    _log.info("Prewarm complete in %.1fs", elapsed)


def start_prewarm() -> None:
    with _lock:
        if _state["ready"] or _state["loading"]:
            return
        _state["loading"] = True
        _state["started_at"] = time.time()
        _state["error"] = None
        _state["steps"] = []

    def _worker() -> None:
        try:
            _run_prewarm()
        except Exception as exc:
            _log.exception("Prewarm failed")
            with _lock:
                _state["error"] = str(exc)
                _state["loading"] = False

    threading.Thread(target=_worker, daemon=True, name="pass-scout-prewarm").start()
