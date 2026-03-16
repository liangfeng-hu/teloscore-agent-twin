import os
from typing import Dict, Literal, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from modes.agent_os import AgentOSMode
from modes.life_os import LifeOSMode


app = FastAPI(title="TelosCore Agent Twin")


class RunRequest(BaseModel):
    mode: Literal["agent_os", "life_os"] = "agent_os"
    user_id: str = Field(default=os.getenv("DEFAULT_USER_ID", "user_001"))
    input: str
    use_llm: bool = False
    llm_backend: Optional[str] = None


class HorizonRequest(BaseModel):
    mode: Literal["agent_os", "life_os"] = "agent_os"
    user_id: str = Field(default=os.getenv("DEFAULT_USER_ID", "user_001"))
    input: str
    steps: int = 4
    use_llm: bool = False
    llm_backend: Optional[str] = None


_RUNNER_POOL: Dict[str, object] = {}


def get_runner(mode: str, user_id: str):
    key = f"{mode}:{user_id}"
    if key not in _RUNNER_POOL:
        if mode == "life_os":
            _RUNNER_POOL[key] = LifeOSMode(user_id=user_id)
        else:
            _RUNNER_POOL[key] = AgentOSMode(user_id=user_id)
    return _RUNNER_POOL[key]


@app.get("/")
def root():
    return {
        "name": "TelosCore Agent Twin",
        "status": "ok",
        "modes": ["agent_os", "life_os"],
        "memory": "EverMemOS + local fallback",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run")
async def run_once(req: RunRequest):
    runner = get_runner(req.mode, req.user_id)
    result = await runner.core.process(
        req.input,
        use_llm=req.use_llm,
        llm_backend=req.llm_backend,
    )
    return result


@app.post("/run_horizon")
async def run_horizon(req: HorizonRequest):
    runner = get_runner(req.mode, req.user_id)

    history = []
    current_prompt = req.input

    for step in range(req.steps):
        result = await runner.core.process(
            current_prompt,
            extra_metadata={"step_index": step + 1, "task_root": req.input},
            use_llm=req.use_llm,
            llm_backend=req.llm_backend,
        )
        history.append({"step": step + 1, **result})

        if req.mode == "life_os":
            if result["action"] == "respond" and result["energy_scalar"] < 0.90 and step >= 1:
                break
            current_prompt = f"请继续围绕这个议题推进下一步：{req.input}"
        else:
            if result["action"] == "respond" and result["energy_scalar"] < 0.95 and step >= 1:
                break
            current_prompt = f"请继续推进该任务，并输出下一步：{req.input}"

    return {
        "mode": req.mode,
        "user_id": req.user_id,
        "steps": len(history),
        "history": history,
    }
