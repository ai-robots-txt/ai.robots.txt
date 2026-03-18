from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "code" / "robots.py"

spec = importlib.util.spec_from_file_location("robots", MODULE_PATH)
robots = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(robots)


def test_list_to_pcre_escapes_regex_metacharacters() -> None:
    # Expected pattern is written explicitly from regex syntax,
    # not derived via re.escape, to keep this test independent.
    agents = ["Bot+One", "Bot(Two)", "Pipe|Name", "Question?"]
    assert robots.list_to_pcre(agents) == r"(Bot\+One|Bot\(Two\)|Pipe\|Name|Question\?)"


def test_list_to_pcre_handles_empty_input() -> None:
    assert robots.list_to_pcre([]) == "()"


def test_json_to_nginx_keeps_robots_txt_unblocked() -> None:
    config = robots.json_to_nginx({"BotA": {}})

    assert 'if ($http_user_agent ~* "(BotA)")' in config
    assert 'if ($request_uri = "/robots.txt")' in config
    assert "return 403;" in config

    # robots.txt allow rule must appear before the final deny block.
    assert config.index('if ($request_uri = "/robots.txt")') < config.index("if ($block)")


def test_json_to_haproxy_outputs_plain_agent_list() -> None:
    assert robots.json_to_haproxy({"AlphaBot": {}, "BetaBot": {}}) == "AlphaBot\nBetaBot"


def test_clean_robot_name_normalizes_non_breaking_hyphen() -> None:
    assert robots.clean_robot_name("Perplexity‑User") == "Perplexity-User"


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
