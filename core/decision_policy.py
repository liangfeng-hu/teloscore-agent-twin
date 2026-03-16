from typing import Tuple

from core.energy_vector import compute_energy
from core.schemas import EnergyVector


def decide_action(ev: EnergyVector, mode: str = "agent_os") -> Tuple[str, str]:
    total = compute_energy(ev)

    if mode == "life_os":
        if ev.U_con > 0.58:
            return "reflect", "high conflict requires reflective repair"
        if ev.U_unc > 0.48:
            return "clarify", "uncertainty is high and needs clarification"
        if ev.U_tel > 0.72:
            return "plan", "telos distance remains high and needs re-alignment"
        if total < 0.95:
            return "respond", "state is stable enough to respond directly"
        return "reflect", "default life-os fallback is reflection"

    if ev.U_con > 0.55:
        return "patch", "historical or current conflict is too high"
    if ev.U_unc > 0.48:
        return "clarify", "uncertainty is too high"
    if ev.U_ent > 0.80:
        return "compress", "context entropy is too high"
    if ev.U_tel > 0.70 and total >= 0.95:
        return "replan", "goal distance remains high and requires replanning"
    if total < 0.95:
        return "respond", "state is stable enough to respond directly"
    return "clarify", "default agent-os fallback is clarification"
