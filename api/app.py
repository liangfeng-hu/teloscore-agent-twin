import os
from typing import Dict, Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from modes.agent_os import AgentOSMode
from modes.life_os import LifeOSMode


app = FastAPI(title="TelosCore Agent Twin")


class RunRequest(BaseModel):
    mode: Literal["agent_os", "life_os"] = "agent_os"
    user_id: str = Field(default=os.getenv("DEFAULT_USER_ID", "user_001"))
    input: str


class HorizonRequest(BaseModel):
    mode: Literal["agent_os", "life_os"] = "agent_os"
    user_id: str = Field(default=os.getenv("DEFAULT_USER_ID", "user_001"))
    input: str
    steps: int = 4


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
    result = await runner.process(req.input)
    return result


@app.post("/run_horizon")
async def run_horizon(req: HorizonRequest):
    runner = get_runner(req.mode, req.user_id)
    history = await runner.run_horizon(req.input, steps=req.steps)
    return {
        "mode": req.mode,
        "user_id": req.user_id,
        "steps": len(history),
        "history": history,
    }
