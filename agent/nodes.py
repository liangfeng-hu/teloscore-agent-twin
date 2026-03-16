from typing import Any, Dict

from agent.tools import maybe_execute_python


async def reasoning_node(runner, prompt: str) -> Dict[str, Any]:
    return await runner.process(prompt)


def tool_node(prompt: str, enable_python: bool = False) -> str | None:
    if not enable_python:
        return None
    return maybe_execute_python(prompt)


def build_followup_prompt(
    mode: str,
    root_task: str,
    result: Dict[str, Any],
    tool_feedback: str | None = None,
) -> str:
    action = result["action"]

    if tool_feedback:
        if tool_feedback.startswith("ERROR:"):
            if mode == "life_os":
                return f"刚才的尝试失败了。请围绕这个议题重新澄清真正阻碍，并给出更稳的下一步：{root_task}"
            return f"刚才的执行暴露出错误。请修补冲突、修正假设，并继续推进任务：{root_task}"

        if tool_feedback.startswith("SUCCESS:"):
            if mode == "life_os":
                return f"刚才的尝试已经产生结果。请基于结果继续推进这个人生议题：{root_task}"
            return f"刚才的执行已成功。请基于结果继续推进任务：{root_task}"

    if mode == "life_os":
        if action == "reflect":
            return f"请继续围绕这个人生议题做深一层反思，并指出真正冲突源：{root_task}"
        if action == "clarify":
            return f"请把这个人生议题中的目标、阻碍、下一步拆清楚：{root_task}"
        if action == "plan":
            return f"请把这个人生议题收敛成温和但明确的三步行动计划：{root_task}"
        return f"请继续围绕这个人生议题给出最小下一步：{root_task}"

    if action == "patch":
        return f"请修补当前冲突并继续推进：{root_task}"
    if action == "clarify":
        return f"请澄清当前目标、约束和成功判据，然后继续推进：{root_task}"
    if action == "compress":
        return f"请压缩上下文，仅保留关键事实与下一步动作：{root_task}"
    if action == "replan":
        return f"请重排优先级，并给出新的三步执行计划：{root_task}"

    return f"请继续推进该任务，并输出最合理的下一步：{root_task}"
