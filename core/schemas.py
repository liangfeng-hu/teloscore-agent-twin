from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


@dataclass
class EnergyVector:
    U_unc: float = 0.18
    U_con: float = 0.12
    U_ent: float = 0.25
    U_tel: float = 0.72

    def clamp(self) -> "EnergyVector":
        self.U_unc = max(0.0, min(1.0, self.U_unc))
        self.U_con = max(0.0, min(1.0, self.U_con))
        self.U_ent = max(0.0, min(1.0, self.U_ent))
        self.U_tel = max(0.0, min(1.0, self.U_tel))
        return self

    def to_dict(self) -> Dict[str, float]:
        return {
            "U_unc": round(self.U_unc, 3),
            "U_con": round(self.U_con, 3),
            "U_ent": round(self.U_ent, 3),
            "U_tel": round(self.U_tel, 3),
        }

    def copy(self) -> "EnergyVector":
        return EnergyVector(**self.to_dict())


@dataclass
class MemoryHit:
    message_id: str
    content: str
    similarity: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "content": self.content,
            "similarity": round(float(self.similarity), 3),
            "metadata": self.metadata,
        }


@dataclass
class ProcessResult:
    mode: str
    action: str
    reason: str
    action_before: str
    reason_before: str
    energy: EnergyVector
    energy_scalar: float
    bias: Dict[str, float]
    memory_hits: int
    memory_preview: List[Dict[str, Any]] = field(default_factory=list)
    pattern_summary: Dict[str, Any] = field(default_factory=dict)
    stored_remote: bool = False
    state_before: Dict[str, float] = field(default_factory=dict)
    state_after: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["energy"] = self.energy.to_dict()
        data["energy_scalar"] = round(self.energy_scalar, 3)
        data["bias"] = {k: round(v, 3) for k, v in self.bias.items()}
        return data
