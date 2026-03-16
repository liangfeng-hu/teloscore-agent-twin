import asyncio
from typing import Dict, Literal

from agent.nodes import build_followup_prompt, reasoning_node, tool_node
from agent.state import AgentRunState, StepTrace
from modes.agent_os import AgentOSMode
from modes.life_os import LifeOSMode


class TelosGraphRunner:
    def __init__(
        self,
        mode: Literal["agent_os", "life_os"] = "agent_os",
        user_id: str = "user_001",
        enable_python: bool = False,
    ) -> None:
        self.mode = mode
        self.user_id = user_id
        self.enable_python = enable_python
        self.runner = LifeOSMode(user_id=user_id) if mode == "life_os" else AgentOSMode(user_id=user_id)

    async def run(self, root_task: str, steps: int = 4) -> Dict:
        state = AgentRunState(
            mode=self.mode,
            root_task=root_task,
            current_prompt=root_task,
        )

        for step in range(1, steps + 1):
            result = await reasoning_node(self.runner, state.current_prompt)
            tool_feedback = tool_node(state.current_prompt, enable_python=self.enable_python)

            trace = StepTrace(
                step=step,
                prompt=state.current_prompt,
                action=result["action"],
                reason=result["reason"],
                energy_scalar=float(result["energy_scalar"]),
                energy=result["energy"],
                memory_hits=int(result["memory_hits"]),
                tool_feedback=tool_feedback,
                raw=result,
            )
            state.traces.append(trace)
            state.steps_taken = step
            state.final_action = result["action"]

            if self._should_stop(step=step, result=result, tool_feedback=tool_feedback):
                break

            state.current_prompt = build_followup_prompt(
                mode=self.mode,
                root_task=root_task,
                result=result,
                tool_feedback=tool_feedback,
            )

        return state.to_dict()

    def _should_stop(self, step: int, result: Dict, tool_feedback: str | None = None) -> bool:
        energy_scalar = float(result["energy_scalar"])
        action = result["action"]

        if tool_feedback and tool_feedback.startswith("SUCCESS:") and step >= 2:
            return True

        if self.mode == "life_os":
            if action == "respond" and energy_scalar < 0.90 and step >= 2:
                return True
            return False

        if action == "respond" and energy_scalar < 0.95 and step >= 2:
            return True
        return False


async def demo():
    runner = TelosGraphRunner(mode="agent_os", user_id="demo_graph", enable_python=False)
    data = await runner.run("为一个上周因定价冲突失败的 AI 产品，规划接下来 7 天的推进方案。", steps=4)
    return data


if __name__ == "__main__":
    out = asyncio.run(demo())
    print(out)
