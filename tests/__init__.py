"""
Architector-LLM Test Suite
"""
import sys
from pathlib import Path

# Automatically ensure backend/src is available on PYTHONPATH for all tests
BACKEND_SRC = Path(__file__).resolve().parent.parent / 'backend' / 'src'
if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))
