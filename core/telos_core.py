from typing import Any, Dict, List, Tuple

from core.decision_policy import decide_action
from core.energy_vector import (
    apply_input_signals,
    apply_memory_bias,
    compute_energy,
    default_energy,
    extract_event_metadata,
)
from core.schemas import EnergyVector, MemoryHit, ProcessResult
from memory.evermemos_client import EverMemOSClient


class TelosCore:
    def __init__(
        self,
        mode: str = "agent_os",
        user_id: str = "user_001",
        memory_client: EverMemOSClient | None = None,
    ) -> None:
        self.mode = mode
        self.user_id = user_id
        self.memory = memory_client or EverMemOSClient()
        self.state = default_energy(mode)

    def reset(self) -> None:
        self.state = default_energy(self.mode)

    def _load_memory_bias(self, user_input: str) -> Tuple[Dict[str, float], List[MemoryHit]]:
        hits = self.memory.search(
            query=user_input,
            user_id=self.user_id,
            top_k=5,
            retrieve_method="hybrid",
        )

        u_con_memory = sum(
            float(hit.metadata.get("conflict", 0)) * float(hit.similarity) for hit in hits
        ) * 0.42

        u_unc_memory = sum(
            float(hit.metadata.get("uncertainty", 0)) * float(hit.similarity) for hit in hits
        ) * 0.34

        u_tel_memory = sum(
            float(hit.metadata.get("telos_bonus", 0.0)) for hit in hits
        ) * 0.18

        bias = {
            "U_con_memory": min(0.75, u_con_memory),
            "U_unc_memory": min(0.65, u_unc_memory),
            "U_tel_memory": max(-0.55, min(0.25, u_tel_memory)),
        }
        return bias, hits

    async def process(
        self,
        user_input: str,
        extra_metadata: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        state_before = self.state.copy()

        apply_input_signals(self.state, user_input, self.mode)
        action_before, reason_before = decide_action(self.state, self.mode)

        bias, hits = self._load_memory_bias(user_input)
        apply_memory_bias(self.state, bias)

        action_after, reason_after = decide_action(self.state, self.mode)
        energy_scalar = compute_energy(self.state)

        event_metadata = extract_event_metadata(user_input, self.mode)
        event_metadata.update(
            {
                "U": round(energy_scalar, 3),
                "U_con_memory": round(bias["U_con_memory"], 3),
                "U_unc_memory": round(bias["U_unc_memory"], 3),
                "U_tel_memory": round(bias["U_tel_memory"], 3),
            }
        )
        if extra_metadata:
            event_metadata.update(extra_metadata)

        stored_remote = self.memory.store(
            content=user_input,
            user_id=self.user_id,
            metadata=event_metadata,
        )
        pattern_summary = self.memory.consolidate_patterns(user_id=self.user_id)

        if action_after in {"patch", "reflect"}:
            self.state.U_con *= 0.35
        if action_after in {"respond", "plan"}:
            self.state.U_tel = max(0.0, self.state.U_tel - 0.05)

        state_after = self.state.copy()

        result = ProcessResult(
            mode=self.mode,
            action=action_after,
            reason=reason_after,
            action_before=action_before,
            reason_before=reason_before,
            energy=self.state.copy(),
            energy_scalar=energy_scalar,
            bias=bias,
            memory_hits=len(hits),
            memory_preview=[hit.to_dict() for hit in hits[:3]],
            pattern_summary=pattern_summary,
            stored_remote=stored_remote,
            state_before=state_before.to_dict(),
            state_after=state_after.to_dict(),
        )
        return result.to_dict()
