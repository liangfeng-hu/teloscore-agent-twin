import asyncio
from pathlib import Path

import matplotlib.pyplot as plt

from modes.agent_os import AgentOSMode
from modes.life_os import LifeOSMode


def plot_history(history, title: str, output_path: str):
    steps = [item["step"] for item in history]
    u_unc = [item["energy"]["U_unc"] for item in history]
    u_con = [item["energy"]["U_con"] for item in history]
    u_ent = [item["energy"]["U_ent"] for item in history]
    u_tel = [item["energy"]["U_tel"] for item in history]

    plt.figure(figsize=(8, 5))
    plt.plot(steps, u_unc, marker="o", label="U_unc")
    plt.plot(steps, u_con, marker="o", label="U_con")
    plt.plot(steps, u_ent, marker="o", label="U_ent")
    plt.plot(steps, u_tel, marker="o", label="U_tel")
    plt.xlabel("Step")
    plt.ylabel("Energy Value")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    Path("assets").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150)
    plt.close()


async def main():
    agent_runner = AgentOSMode(user_id="plot_agent")
    life_runner = LifeOSMode(user_id="plot_life")

    agent_task = "为一个上周因定价冲突失败的 AI 产品，规划接下来 7 天的推进方案。"
    life_task = "我总是因为拖延和焦虑，把最重要的人生目标往后推。"

    agent_history = await agent_runner.run_horizon(agent_task, steps=4)
    life_history = await life_runner.run_horizon(life_task, steps=4)

    plot_history(
        history=agent_history,
        title="Agent OS Energy Trace",
        output_path="assets/energy_trace_agent.png",
    )
    plot_history(
        history=life_history,
        title="Life OS Energy Trace",
        output_path="assets/energy_trace_life.png",
    )

    print("Saved:")
    print(" - assets/energy_trace_agent.png")
    print(" - assets/energy_trace_life.png")


if __name__ == "__main__":
    asyncio.run(main())
