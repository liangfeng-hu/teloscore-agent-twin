from typing import Dict, List

from core.schemas import MemoryHit


def load_bias_from_hits(hits: List[MemoryHit]) -> Dict[str, float]:
    """
    把检索回来的记忆命中，转成 U 向量偏置。
    """
    u_con_memory = 0.0
    u_unc_memory = 0.0
    u_tel_memory = 0.0

    for hit in hits:
        sim = float(hit.similarity)
        meta = hit.metadata or {}

        u_con_memory += float(meta.get("conflict", 0)) * sim * 0.42
        u_unc_memory += float(meta.get("uncertainty", 0)) * sim * 0.34
        u_tel_memory += float(meta.get("telos_bonus", 0.0)) * 0.18

    return {
        "U_con_memory": min(0.75, round(u_con_memory, 3)),
        "U_unc_memory": min(0.65, round(u_unc_memory, 3)),
        "U_tel_memory": max(-0.55, min(0.25, round(u_tel_memory, 3))),
    }


def preview_hits(hits: List[MemoryHit], limit: int = 3) -> List[Dict]:
    return [hit.to_dict() for hit in hits[:limit]]
