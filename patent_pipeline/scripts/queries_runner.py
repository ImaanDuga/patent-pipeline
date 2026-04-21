"""
Thin wrapper so 05_reports.py can import run_all without
relying on the '04_queries' filename prefix.
"""
from importlib import util
import os

_spec = util.spec_from_file_location(
    "queries_module",
    os.path.join(os.path.dirname(__file__), "04_queries.py")
)
_mod = util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

run_all = _mod.run_all
