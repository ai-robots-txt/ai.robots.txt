from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "code" / "robots.py"

spec = importlib.util.spec_from_file_location("robots", MODULE_PATH)
robots = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(robots)


def test_json_to_txt_preserves_agent_order() -> None:
    robots_txt = robots.json_to_txt({"BotA": {}, "BotB": {}})

    assert robots_txt == "User-agent: BotA\nUser-agent: BotB\nDisallow: /\n"


def test_json_to_txt_handles_empty_input() -> None:
    assert robots.json_to_txt({}) == "\nDisallow: /\n"


def test_list_to_pcre_escapes_special_characters() -> None:
    items = ["Bot+One", "Bot(Two)"]

    assert robots.list_to_pcre(items) == r"(Bot\+One|Bot\(Two\))"


def test_list_to_pcre_supports_dict_keys_iterable() -> None:
    agents = {"Bot+One": {}, "Bot(Two)": {}}

    assert robots.list_to_pcre(agents.keys()) == r"(Bot\+One|Bot\(Two\))"


def test_list_to_pcre_handles_empty_input() -> None:
    assert robots.list_to_pcre([]) == "()"


def test_escape_md_escapes_markdown_specials() -> None:
    value = "A_B+C[Z]-!"

    assert robots.escape_md(value) == r"A\_B\+C\[Z\]\-\!"


def test_clean_robot_name_normalizes_non_breaking_hyphen() -> None:
    assert robots.clean_robot_name("Perplexity‑User") == "Perplexity-User"


def test_clean_robot_name_keeps_regular_names_unchanged() -> None:
    assert robots.clean_robot_name("NormalBot") == "NormalBot"


def test_update_file_if_changed_writes_new_content_when_different() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / "robots.txt"
        target.write_text("old", encoding="utf-8")

        old_loader = robots.load_robots_json
        try:
            robots.load_robots_json = lambda: {"BotA": {}}
            robots.update_file_if_changed(
                str(target),
                lambda robots_json: robots.json_to_txt(robots_json),
            )
        finally:
            robots.load_robots_json = old_loader

        assert target.read_text(encoding="utf-8") == "User-agent: BotA\nDisallow: /\n"


def test_update_file_if_changed_keeps_file_when_content_same() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / "robots.txt"
        target.write_text("constant", encoding="utf-8")

        old_loader = robots.load_robots_json
        try:
            robots.load_robots_json = lambda: {"ignored": {}}
            robots.update_file_if_changed(str(target), lambda _robots_json: "constant")
        finally:
            robots.load_robots_json = old_loader

        assert target.read_text(encoding="utf-8") == "constant"
