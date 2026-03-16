import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

import requests

from core.schemas import MemoryHit


class EverMemOSClient:
    """
    优先走 EverMemOS 接口；
    如果远端服务没起来，就自动回退到本地 JSONL。
    """

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int | None = None,
        local_path: str | None = None,
    ) -> None:
        self.base_url = (base_url or os.getenv("EVERMEMOS_BASE_URL", "http://localhost:1995")).rstrip("/")
        self.timeout = int(timeout or os.getenv("EVERMEMOS_TIMEOUT", "5"))
        self.local_path = Path(local_path or os.getenv("LOCAL_MEMORY_PATH", ".local_memory/memory.jsonl"))
        self.local_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.local_path.exists():
            self.local_path.touch()

    def health(self) -> bool:
        try:
            resp = requests.get(f"{self.base_url}/health", timeout=self.timeout)
            return resp.ok
        except requests.RequestException:
            return False

    def store(
        self,
        content: str,
        user_id: str = "user_001",
        metadata: Dict[str, Any] | None = None,
        message_id: str | None = None,
    ) -> bool:
        payload = {
            "message_id": message_id or f"msg_{uuid4().hex[:12]}",
            "create_time": datetime.now(timezone.utc).isoformat(),
            "sender": user_id,
            "content": content,
            "metadata": metadata or {},
        }

        remote_ok = self._store_remote(payload)
        self._store_local(payload)
        return remote_ok

    def search(
        self,
        query: str,
        user_id: str = "user_001",
        top_k: int = 5,
        retrieve_method: str = "hybrid",
    ) -> List[MemoryHit]:
        remote_hits = self._search_remote(
            query=query,
            user_id=user_id,
            top_k=top_k,
            retrieve_method=retrieve_method,
        )
        if remote_hits:
            return remote_hits[:top_k]

        local_hits = self._search_local(query=query, user_id=user_id, top_k=top_k)
        return local_hits[:top_k]

    def consolidate_patterns(self, user_id: str = "user_001") -> Dict[str, int]:
        rows = self._load_local()
        rows = [r for r in rows if r.get("sender") == user_id]
        return {
            "count": len(rows),
            "conflict_events": sum(1 for r in rows if int(r.get("metadata", {}).get("conflict", 0)) > 0),
            "uncertainty_events": sum(1 for r in rows if int(r.get("metadata", {}).get("uncertainty", 0)) > 0),
            "goal_events": sum(1 for r in rows if float(r.get("metadata", {}).get("telos_bonus", 0.0)) < 0),
        }

    def _store_remote(self, payload: Dict[str, Any]) -> bool:
        try:
            resp = requests.post(
                f"{self.base_url}/api/v1/memories",
                json=payload,
                timeout=self.timeout,
            )
            return resp.ok
        except requests.RequestException:
            return False

    def _search_remote(
        self,
        query: str,
        user_id: str,
        top_k: int,
        retrieve_method: str,
    ) -> List[MemoryHit]:
        try:
            resp = requests.request(
                "GET",
                f"{self.base_url}/api/v1/memories/search",
                json={
                    "query": query,
                    "user_id": user_id,
                    "retrieve_method": retrieve_method,
                    "top_k": top_k,
                },
                timeout=self.timeout,
            )
            if not resp.ok:
                return []

            data = resp.json()
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                items = (
                    data.get("data")
                    or data.get("items")
                    or data.get("results")
                    or data.get("memories")
                    or []
                )
            else:
                items = []

            hits: List[MemoryHit] = []
            for item in items:
                content = item.get("content") or item.get("text") or item.get("memory") or ""
                similarity = float(item.get("similarity", item.get("score", 0.0)))
                metadata = item.get("metadata", {}) or {}
                message_id = item.get("message_id", f"remote_{uuid4().hex[:8]}")
                if not content:
                    continue
                hits.append(
                    MemoryHit(
                        message_id=message_id,
                        content=content,
                        similarity=similarity,
                        metadata=metadata,
                    )
                )
            return hits
        except (requests.RequestException, ValueError, TypeError):
            return []

    def _store_local(self, payload: Dict[str, Any]) -> None:
        with self.local_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def _search_local(self, query: str, user_id: str, top_k: int) -> List[MemoryHit]:
        rows = self._load_local()
        rows = [r for r in rows if r.get("sender") == user_id]

        scored: List[MemoryHit] = []
        for row in rows:
            content = row.get("content", "")
            score = self._similarity(query, content)
            if score <= 0:
                continue
            scored.append(
                MemoryHit(
                    message_id=row.get("message_id", f"local_{uuid4().hex[:8]}"),
                    content=content,
                    similarity=score,
                    metadata=row.get("metadata", {}) or {},
                )
            )

        scored.sort(key=lambda x: x.similarity, reverse=True)
        return scored[:top_k]

    def _load_local(self) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        with self.local_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return rows

    def _similarity(self, query: str, text: str) -> float:
        q_tokens = self._tokenize(query)
        t_tokens = self._tokenize(text)
        if not q_tokens or not t_tokens:
            return 0.0

        overlap = len(q_tokens & t_tokens)
        base = overlap / max(1.0, (len(q_tokens) * len(t_tokens)) ** 0.5)

        substring_bonus = 0.0
        q_short = query.strip().lower()
        t_low = text.strip().lower()
        if q_short and q_short[:12] in t_low:
            substring_bonus = 0.25

        return round(min(1.0, base + substring_bonus), 3)

    def _tokenize(self, text: str) -> set[str]:
        text = text.lower()
        ascii_tokens = re.sub(r"[^\w\u4e00-\u9fff]+", " ", text).split()
        zh_chars = [ch for ch in text if "\u4e00" <= ch <= "\u9fff"]
        return set(ascii_tokens + zh_chars)
