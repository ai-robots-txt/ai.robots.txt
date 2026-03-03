from __future__ import annotations

import importlib.util
import re
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "code" / "robots.py"

spec = importlib.util.spec_from_file_location("robots", MODULE_PATH)
robots = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(robots)


def test_json_to_txt_preserves_order():
    robots_txt = robots.json_to_txt({"BotA": {}, "BotB": {}})
    assert robots_txt == "User-agent: BotA\nUser-agent: BotB\nDisallow: /\n"


def test_list_to_pcre_escapes_special_characters():
    items = ["Bot+One", "Bot(Two)"]
    expected = f"({"|".join(map(re.escape, items))})"
    assert robots.list_to_pcre(items) == expected


def test_json_to_nginx_includes_robots_txt_exception():
    config = robots.json_to_nginx({"BotA": {}})
    assert "if ($request_uri = \"/robots.txt\")" in config
