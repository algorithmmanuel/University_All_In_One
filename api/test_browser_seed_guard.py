"""Guard the browser fixture against accidental execution during test discovery."""
import ast
from pathlib import Path


def test_browser_seed_is_entrypoint_guarded():
    source = Path(__file__).with_name("seed_browser_test.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    # Database seeding is invoked only through an explicit __main__ guard.
    top_level_calls = [node for node in tree.body if isinstance(node, ast.Expr) and
                       isinstance(node.value, ast.Call)]
    assert not top_level_calls
    guards = [node for node in tree.body if isinstance(node, ast.If) and
              isinstance(node.test, ast.Compare) and
              isinstance(node.test.left, ast.Name) and
              node.test.left.id == "__name__"]
    assert guards
