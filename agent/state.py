from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StepTrace:
    step: int
    prompt: str
    action: str
    reason: str
    energy_scalar: float
    energy: Dict[str, float]
    memory_hits: int
    tool_feedback: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step,
            "prompt": self.prompt,
            "action": self.action,
            "reason": self.reason,
            "energy_scalar": round(self.energy_scalar, 3),
            "energy": self.energy,
            "memory_hits": self.memory_hits,
            "tool_feedback": self.tool_feedback,
            "raw": self.raw,
        }


@dataclass
class AgentRunState:
    mode: str
    root_task: str
    current_prompt: str
    traces: List[StepTrace] = field(default_factory=list)
    steps_taken: int = 0
    final_action: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "root_task": self.root_task,
            "current_prompt": self.current_prompt,
            "steps_taken": self.steps_taken,
            "final_action": self.final_action,
            "history": [t.to_dict() for t in self.traces],
        }
