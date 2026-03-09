from __future__ import annotations

import importlib.util
import re
import tempfile
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "code" / "robots.py"

spec = importlib.util.spec_from_file_location("robots", MODULE_PATH)
robots = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(robots)


def test_json_to_txt_preserves_order():
    robots_txt = robots.json_to_txt({"BotA": {}, "BotB": {}})
    assert robots_txt == "User-agent: BotA\nUser-agent: BotB\nDisallow: /\n"


def test_json_to_txt_handles_empty_input():
    assert robots.json_to_txt({}) == "\nDisallow: /\n"


def test_list_to_pcre_escapes_special_characters():
    items = ["Bot+One", "Bot(Two)"]
    expected = f"({'|'.join(map(re.escape, items))})"
    assert robots.list_to_pcre(items) == expected


def test_list_to_pcre_supports_dict_keys_iterable():
    agents = {"Bot+One": {}, "Bot(Two)": {}}
    expected = f"({'|'.join(map(re.escape, agents.keys()))})"
    assert robots.list_to_pcre(agents.keys()) == expected


def test_json_to_htaccess_contains_rewrite_rules_and_robots_exception():
    config = robots.json_to_htaccess({"Bot+One": {}, "Bot(Two)": {}})
    assert config.startswith("RewriteEngine On\n")
    assert "RewriteCond %{HTTP_USER_AGENT} (Bot\\+One|Bot\\(Two\\)) [NC]" in config
    assert "RewriteRule !^/?robots\\.txt$ - [F]" in config


def test_json_to_nginx_includes_robots_txt_exception():
    config = robots.json_to_nginx({"BotA": {}})
    assert "if ($request_uri = \"/robots.txt\")" in config
    assert "if ($block)" in config
    assert "return 403;" in config


def test_json_to_lighttpd_contains_user_agent_and_robots_exception():
    config = robots.json_to_lighttpd({"BotA": {}})
    assert '$HTTP["url"] != "/robots.txt"' in config
    assert '$HTTP["user-agent"] =~ "(BotA)"' in config


def test_json_to_caddy_contains_user_agent_matcher():
    config = robots.json_to_caddy({"BotA": {}, "BotB": {}})
    assert config.startswith("@aibots {")
    assert 'header_regexp User-Agent "(BotA|BotB)"' in config
    assert config.strip().endswith("}")


def test_json_to_haproxy_emits_one_agent_per_line():
    config = robots.json_to_haproxy({"BotA": {}, "BotB": {}})
    assert config == "BotA\nBotB"


def test_escape_md_escapes_markdown_specials():
    value = "A_B+C[Z]-!"
    escaped = robots.escape_md(value)
    assert escaped == r"A\_B\+C\[Z\]\-\!"


def test_json_to_table_renders_expected_row():
    robots_json = {
        "BotA": {
            "operator": "Op",
            "respect": "Yes",
            "function": "Crawler",
            "frequency": "Daily",
            "description": "Desc",
        }
    }
    table = robots.json_to_table(robots_json)
    assert table.startswith("| Name | Operator |")
    assert "| BotA | Op | Yes | Crawler | Daily | Desc |" in table


def test_json_to_table_escapes_markdown_in_name():
    robots_json = {
        "Bot_[A]": {
            "operator": "Op",
            "respect": "Yes",
            "function": "Crawler",
            "frequency": "Daily",
            "description": "Desc",
        }
    }
    table = robots.json_to_table(robots_json)
    assert "Bot\\_\\[A\\]" in table


def test_clean_robot_name_normalizes_non_breaking_hyphen():
    assert robots.clean_robot_name("Perplexity‑User") == "Perplexity-User"


def test_clean_robot_name_keeps_regular_names_unchanged():
    assert robots.clean_robot_name("NormalBot") == "NormalBot"


def test_update_file_if_changed_writes_new_content_when_different():
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


def test_update_file_if_changed_keeps_file_when_content_same():
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
