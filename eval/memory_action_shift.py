import asyncio
import json
from pathlib import Path
from uuid import uuid4

from core.telos_core import TelosCore
from memory.evermemos_client import EverMemOSClient


async def main():
    local_path = f".local_memory/eval_shift_{uuid4().hex}.jsonl"
    Path(".local_memory").mkdir(parents=True, exist_ok=True)

    memory_client = EverMemOSClient(local_path=local_path)

    baseline = TelosCore(
        mode="agent_os",
        user_id="baseline_user",
        memory_client=memory_client,
    )
    seeded = TelosCore(
        mode="agent_os",
        user_id="seeded_user",
        memory_client=memory_client,
    )

    memory_client.store(
        content="上周这个项目因为定价策略冲突失败，团队在关键节点做了错误决策。",
        user_id="seeded_user",
        metadata={"conflict": 1, "uncertainty": 0, "telos_bonus": 0.12, "mode": "agent_os"},
    )
    memory_client.store(
        content="曾经在推进类似任务时，因为目标和价格策略没有澄清清楚，最终导致失败。",
        user_id="seeded_user",
        metadata={"conflict": 1, "uncertainty": 1, "telos_bonus": 0.08, "mode": "agent_os"},
    )

    query = "为一个上周因定价冲突失败的 AI 产品，规划接下来 7 天的推进方案。"

    baseline_result = await baseline.process(query)
    seeded_result = await seeded.process(query)

    summary = {
        "query": query,
        "baseline": {
            "action": baseline_result["action"],
            "energy_scalar": baseline_result["energy_scalar"],
            "bias": baseline_result["bias"],
            "memory_hits": baseline_result["memory_hits"],
        },
        "seeded": {
            "action": seeded_result["action"],
            "energy_scalar": seeded_result["energy_scalar"],
            "bias": seeded_result["bias"],
            "memory_hits": seeded_result["memory_hits"],
        },
        "interpretation": "如果 seeded 的 U_con_memory 更高，并导致 action 更偏向 patch / clarify，就说明记忆确实改变了动作选择。",
    }

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
