from typing import Any, Dict, List

from core.telos_core import TelosCore


class LifeOSMode:
    def __init__(self, user_id: str = "user_001") -> None:
        self.mode = "life_os"
        self.core = TelosCore(mode=self.mode, user_id=user_id)

    async def process(self, user_input: str) -> Dict[str, Any]:
        return await self.core.process(user_input)

    async def run_horizon(self, topic: str, steps: int = 4) -> List[Dict[str, Any]]:
        history: List[Dict[str, Any]] = []
        current_prompt = topic

        for step in range(steps):
            result = await self.core.process(
                current_prompt,
                extra_metadata={"step_index": step + 1, "life_topic_root": topic},
            )
            history.append({"step": step + 1, **result})

            if result["action"] == "respond" and result["energy_scalar"] < 0.90 and step >= 1:
                break

            current_prompt = self._next_prompt(topic, result, step + 1)

        return history

    def _next_prompt(self, topic: str, result: Dict[str, Any], step: int) -> str:
        action = result["action"]

        if action == "reflect":
            return f"请围绕这个人生议题做更深一层反思，并指出真正冲突源头：{topic}"
        if action == "clarify":
            return f"请帮我澄清这个议题中的真实目标、阻碍和可行动点：{topic}"
        if action == "plan":
            return f"请把这个人生议题改写为一个温和但明确的三步计划：{topic}"

        return f"请继续围绕这个议题给出下一步最小行动：{topic}"
