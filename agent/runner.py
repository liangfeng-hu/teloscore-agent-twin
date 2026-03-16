import argparse
import asyncio
import json

from agent.graph import TelosGraphRunner


async def main():
    parser = argparse.ArgumentParser(description="Run TelosCore Agent Twin state machine.")
    parser.add_argument("--mode", choices=["agent_os", "life_os"], default="agent_os")
    parser.add_argument("--user_id", default="cli_user")
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument("--enable_python", action="store_true")
    parser.add_argument("--input", required=True)

    args = parser.parse_args()

    runner = TelosGraphRunner(
        mode=args.mode,
        user_id=args.user_id,
        enable_python=args.enable_python,
    )
    result = await runner.run(root_task=args.input, steps=args.steps)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
