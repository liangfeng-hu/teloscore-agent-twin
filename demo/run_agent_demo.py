import asyncio
import json

from modes.agent_os import AgentOSMode


async def main():
    runner = AgentOSMode(user_id="demo_agent")

    task = "为一个上周因定价冲突失败的 AI 产品，规划接下来 7 天的推进方案，并避免再次犯同样的错误。"
    history = await runner.run_horizon(task, steps=4)

    print("\n=== Agent OS Demo ===")
    for item in history:
        print(
            f"Step {item['step']} | "
            f"Action={item['action']} | "
            f"Energy={item['energy_scalar']} | "
            f"Hits={item['memory_hits']} | "
            f"Reason={item['reason']}"
        )

    print("\n=== Final JSON ===")
    print(json.dumps(history[-1], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
