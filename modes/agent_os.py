from typing import Any, Dict, List

from core.telos_core import TelosCore


class AgentOSMode:
    def __init__(self, user_id: str = "user_001") -> None:
        self.mode = "agent_os"
        self.core = TelosCore(mode=self.mode, user_id=user_id)

    async def process(self, user_input: str) -> Dict[str, Any]:
        return await self.core.process(user_input)

    async def run_horizon(self, task: str, steps: int = 4) -> List[Dict[str, Any]]:
        history: List[Dict[str, Any]] = []
        current_prompt = task

        for step in range(steps):
            result = await self.core.process(
                current_prompt,
                extra_metadata={"step_index": step + 1, "task_root": task},
            )
            history.append({"step": step + 1, **result})

            if result["action"] == "respond" and result["energy_scalar"] < 0.95 and step >= 1:
                break

            current_prompt = self._next_prompt(task, result, step + 1)

        return history

    def _next_prompt(self, task: str, result: Dict[str, Any], step: int) -> str:
        action = result["action"]

        if action == "patch":
            return f"请修补上一步中暴露出的冲突，并继续推进任务：{task}"
        if action == "clarify":
            return f"请澄清目标、约束和成功判据，然后继续推进：{task}"
        if action == "compress":
            return f"请压缩上下文，只保留关键事实和下一步动作：{task}"
        if action == "replan":
            return f"请重排优先级，并给出新的三步执行计划：{task}"

        return f"请继续推进该任务，并输出最合理的下一步：{task}"
