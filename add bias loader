from typing import List

from core.schemas import MemoryHit
from memory.evermemos_client import EverMemOSClient


def retrieve_memories(
    query: str,
    user_id: str,
    top_k: int = 5,
    client: EverMemOSClient | None = None,
) -> List[MemoryHit]:
    mem = client or EverMemOSClient()
    return mem.search(query=query, user_id=user_id, top_k=top_k, retrieve_method="hybrid")


def retrieve_preview(
    query: str,
    user_id: str,
    top_k: int = 5,
    client: EverMemOSClient | None = None,
) -> list[dict]:
    hits = retrieve_memories(query=query, user_id=user_id, top_k=top_k, client=client)
    return [hit.to_dict() for hit in hits]
