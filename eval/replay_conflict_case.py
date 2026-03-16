import asyncio
import json
from pathlib import Path
from uuid import uuid4

from core.telos_core import TelosCore
from memory.evermemos_client import EverMemOSClient


async def main():
    local_path = f".local_memory/eval_replay_{uuid4().hex}.jsonl"
    Path(".local_memory").mkdir(parents=True, exist_ok=True)

    memory_client = EverMemOSClient(local_path=local_path)
    core = TelosCore(mode="agent_os", user_id="replay_user", memory_client=memory_client)

    seed_event = "上次推进这个项目时，因为约束没有澄清清楚，产生了严重冲突和失败。"
    memory_client.store(
        content=seed_event,
        user_id="replay_user",
        metadata={"conflict": 1, "uncertainty": 1, "telos_bonus": 0.10, "mode": "agent_os"},
    )

    prompts = [
        "请推进这个项目的下一步。",
        "请继续推进这个项目，但注意不要重复之前的错误。",
        "请基于已有冲突经验，重新规划这个项目的三步执行路线。",
    ]

    history = []
    for p in prompts:
        result = await core.process(p)
        history.append(
            {
                "prompt": p,
                "action": result["action"],
                "energy_scalar": result["energy_scalar"],
                "bias": result["bias"],
                "memory_hits": result["memory_hits"],
            }
        )

    print(json.dumps(history, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
