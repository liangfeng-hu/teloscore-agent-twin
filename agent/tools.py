import re
import subprocess
import sys
import tempfile
from pathlib import Path


PYTHON_BLOCK_RE = re.compile(r"```python\s*(.*?)```", re.DOTALL | re.IGNORECASE)


def extract_python_block(text: str) -> str | None:
    match = PYTHON_BLOCK_RE.search(text)
    if not match:
        return None
    return match.group(1).strip()


def should_execute_python(prompt: str) -> bool:
    return extract_python_block(prompt) is not None


def execute_python_code(code_str: str, timeout_seconds: int = 8) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = Path(tmpdir) / "snippet.py"
        script_path.write_text(code_str, encoding="utf-8")

        try:
            proc = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            return "ERROR:\nExecution timed out."

        stdout = (proc.stdout or "").strip()
        stderr = (proc.stderr or "").strip()

        if proc.returncode == 0:
            if not stdout:
                stdout = "(no stdout)"
            return f"SUCCESS:\n{stdout}"

        return f"ERROR:\n{stderr or 'Unknown execution error.'}"


def maybe_execute_python(prompt: str) -> str | None:
    code = extract_python_block(prompt)
    if not code:
        return None
    return execute_python_code(code)
