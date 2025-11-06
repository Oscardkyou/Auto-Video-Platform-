import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from workflows.workers.worker import main


if __name__ == "__main__":
    asyncio.run(main())
