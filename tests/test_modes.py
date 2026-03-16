import asyncio
import unittest

from modes.agent_os import AgentOSMode
from modes.life_os import LifeOSMode


class TestModes(unittest.TestCase):
    def test_agent_mode_runs(self):
        async def _run():
            runner = AgentOSMode(user_id="test_agent_mode")
            result = await runner.process("请推进这个有冲突风险的项目。")
            self.assertIn(result["action"], {"patch", "clarify", "compress", "replan", "respond"})
        asyncio.run(_run())

    def test_life_mode_runs(self):
        async def _run():
            runner = LifeOSMode(user_id="test_life_mode")
            result = await runner.process("我在家庭和个人目标之间很冲突。")
            self.assertIn(result["action"], {"reflect", "clarify", "plan", "respond"})
        asyncio.run(_run())


if __name__ == "__main__":
    unittest.main()
