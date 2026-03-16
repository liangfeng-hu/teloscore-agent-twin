import asyncio
import unittest
from pathlib import Path
from uuid import uuid4

from core.telos_core import TelosCore
from memory.evermemos_client import EverMemOSClient


class TestMemoryBias(unittest.TestCase):
    def test_seeded_memory_changes_bias(self):
        async def _run():
            Path(".local_memory").mkdir(parents=True, exist_ok=True)
            local_path = f".local_memory/test_bias_{uuid4().hex}.jsonl"
            client = EverMemOSClient(local_path=local_path)

            baseline = TelosCore(mode="agent_os", user_id="u_base", memory_client=client)
            seeded = TelosCore(mode="agent_os", user_id="u_seed", memory_client=client)

            client.store(
                content="这个项目曾因严重冲突失败。",
                user_id="u_seed",
                metadata={"conflict": 1, "uncertainty": 0, "telos_bonus": 0.10, "mode": "agent_os"},
            )

            query = "请推进这个项目的下一步。"
            r_base = await baseline.process(query)
            r_seed = await seeded.process(query)

            self.assertGreaterEqual(r_seed["bias"]["U_con_memory"], r_base["bias"]["U_con_memory"])

        asyncio.run(_run())


if __name__ == "__main__":
    unittest.main()
