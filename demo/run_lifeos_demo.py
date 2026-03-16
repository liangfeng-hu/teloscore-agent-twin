import asyncio
import json

from modes.life_os import LifeOSMode


async def main():
    runner = LifeOSMode(user_id="demo_life")

    topic = "我总是因为拖延和焦虑，把最重要的人生目标往后推，明明知道该做却总卡住。"
    history = await runner.run_horizon(topic, steps=4)

    print("\n=== Life OS Demo ===")
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
