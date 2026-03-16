from typing import Dict

from core.schemas import EnergyVector


CONFLICT_HINTS = (
    "错", "错误", "冲突", "失败", "不对", "矛盾", "卡住", "风险",
    "wrong", "error", "conflict", "failed", "failure", "bug", "stuck", "risk"
)

UNCERTAINTY_HINTS = (
    "也许", "可能", "不确定", "不清楚", "模糊",
    "maybe", "unclear", "unsure", "uncertain", "not sure"
)

GOAL_HINTS = (
    "目标", "计划", "推进", "收敛", "完成", "下一步", "里程碑", "执行",
    "goal", "plan", "milestone", "execute", "next step", "ship"
)

LIFE_HINTS = (
    "家庭", "焦虑", "习惯", "拖延", "关系", "睡眠", "情绪", "人生", "生活",
    "family", "anxiety", "habit", "procrastination", "relationship", "sleep", "life"
)


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(k.lower() in lower for k in keywords)


def default_energy(mode: str = "agent_os") -> EnergyVector:
    if mode == "life_os":
        return EnergyVector(U_unc=0.16, U_con=0.15, U_ent=0.22, U_tel=0.68)
    return EnergyVector(U_unc=0.18, U_con=0.12, U_ent=0.25, U_tel=0.72)


def compute_energy(ev: EnergyVector) -> float:
    return (
        1.2 * ev.U_unc +
        1.8 * ev.U_con +
        1.0 * ev.U_ent +
        1.4 * ev.U_tel
    )


def apply_input_signals(ev: EnergyVector, user_input: str, mode: str = "agent_os") -> EnergyVector:
    lower = user_input.lower()

    if _contains_any(lower, CONFLICT_HINTS):
        ev.U_con += 0.28

    if _contains_any(lower, UNCERTAINTY_HINTS):
        ev.U_unc += 0.22

    ev.U_ent += min(0.18, len(user_input) / 240.0)

    if _contains_any(lower, GOAL_HINTS):
        ev.U_tel -= 0.12
    else:
        ev.U_tel += 0.04

    if mode == "life_os" and _contains_any(lower, LIFE_HINTS):
        ev.U_con += 0.12
        ev.U_tel += 0.05

    return ev.clamp()


def apply_memory_bias(ev: EnergyVector, bias: Dict[str, float]) -> EnergyVector:
    ev.U_con += bias.get("U_con_memory", 0.0)
    ev.U_unc += bias.get("U_unc_memory", 0.0)
    ev.U_tel += bias.get("U_tel_memory", 0.0)
    return ev.clamp()


def extract_event_metadata(user_input: str, mode: str = "agent_os") -> Dict[str, float | int | str]:
    lower = user_input.lower()

    conflict = 1 if _contains_any(lower, CONFLICT_HINTS) else 0
    uncertainty = 1 if _contains_any(lower, UNCERTAINTY_HINTS) else 0

    if _contains_any(lower, GOAL_HINTS):
        telos_bonus = -0.18
    else:
        telos_bonus = 0.05

    if mode == "life_os" and _contains_any(lower, LIFE_HINTS):
        telos_bonus -= 0.05

    return {
        "conflict": conflict,
        "uncertainty": uncertainty,
        "telos_bonus": round(telos_bonus, 3),
        "mode": mode,
        "text_len": len(user_input),
    }
