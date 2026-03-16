from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List


class TopologicalMemory:
    """
    一个轻量拓扑记忆摘要器。
    """

    def __init__(self, half_life_hours: float = 72.0) -> None:
        self.half_life_hours = half_life_hours

    def summarize(self, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        weighted_conflict = 0.0
        weighted_uncertainty = 0.0
        weighted_goal = 0.0

        for row in rows:
            meta = row.get("metadata", {}) or {}
            w = self._decay_weight(row.get("create_time"))
            weighted_conflict += float(meta.get("conflict", 0)) * w
            weighted_uncertainty += float(meta.get("uncertainty", 0)) * w
            weighted_goal += 1.0 * w if float(meta.get("telos_bonus", 0.0)) < 0 else 0.0

        dominant = "neutral"
        if weighted_conflict >= max(weighted_uncertainty, weighted_goal) and weighted_conflict > 0:
            dominant = "conflict"
        elif weighted_uncertainty >= max(weighted_conflict, weighted_goal) and weighted_uncertainty > 0:
            dominant = "uncertainty"
        elif weighted_goal > 0:
            dominant = "goal"

        return {
            "weighted_conflict": round(weighted_conflict, 3),
            "weighted_uncertainty": round(weighted_uncertainty, 3),
            "weighted_goal": round(weighted_goal, 3),
            "dominant_motif": dominant,
            "count": len(rows),
        }

    def _decay_weight(self, iso_ts: str | None) -> float:
        if not iso_ts:
            return 1.0
        try:
            dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            hours = max(0.0, (now - dt).total_seconds() / 3600.0)
            return 0.5 ** (hours / self.half_life_hours)
        except Exception:
            return 1.0
