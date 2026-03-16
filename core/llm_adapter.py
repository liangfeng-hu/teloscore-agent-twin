from typing import Optional


def generate_with_template(action: str, user_input: str, mode: str) -> str:
    """
    当前最小可落地版本：
    不调用外部 LLM，直接根据 action 生成可展示的具体输出文本。
    """

    if mode == "life_os":
        if action == "reflect":
            return (
                "【Reflect】\n"
                f"围绕议题：{user_input}\n"
                "1. 先区分表层压力与深层冲突。\n"
                "2. 找出真正的阻碍，不要只盯着症状。\n"
                "3. 给出一个今天就能执行的最小行动。"
            )
        if action == "clarify":
            return (
                "【Clarify】\n"
                f"围绕议题：{user_input}\n"
                "请澄清：\n"
                "- 你真正想达到的目标是什么？\n"
                "- 当前最大的阻碍是什么？\n"
                "- 下一步最小行动是什么？"
            )
        if action == "plan":
            return (
                "【Plan】\n"
                f"围绕议题：{user_input}\n"
                "三步计划：\n"
                "1. 写下真实目标。\n"
                "2. 列出唯一最关键阻碍。\n"
                "3. 今天完成一个 10 分钟以内的小动作。"
            )
        return (
            "【Respond】\n"
            f"围绕议题：{user_input}\n"
            "请保持当前方向，继续做最小下一步。"
        )

    if action == "patch":
        return (
            "【Patch】\n"
            f"任务：{user_input}\n"
            "请修补当前冲突点，并输出：\n"
            "1. 冲突来源\n"
            "2. 修正假设\n"
            "3. 修正后的三步执行方案"
        )
    if action == "clarify":
        return (
            "【Clarify】\n"
            f"任务：{user_input}\n"
            "请先澄清：\n"
            "1. 目标\n"
            "2. 约束\n"
            "3. 成功判据\n"
            "然后再推进。"
        )
    if action == "compress":
        return (
            "【Compress】\n"
            f"任务：{user_input}\n"
            "请压缩上下文，仅保留关键事实、当前风险、下一步动作。"
        )
    if action == "replan":
        return (
            "【Replan】\n"
            f"任务：{user_input}\n"
            "请重新排列优先级，并输出新的三步计划。"
        )
    return (
        "【Respond】\n"
        f"任务：{user_input}\n"
        "当前状态可直接推进，请给出最合理的下一步。"
    )


def generate_with_llm(action: str, user_input: str, mode: str, backend: Optional[str] = None) -> str:
    """
    现在先做占位。
    后续你接 Ollama 或 OpenAI，就在这里替换。
    """
    return generate_with_template(action=action, user_input=user_input, mode=mode)
