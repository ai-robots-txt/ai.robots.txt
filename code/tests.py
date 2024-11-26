"""These tests can be run with pytest.
This requires pytest: pip install pytest
cd to the `code` directory and run `pytest`
"""

import json
from pathlib import Path

from dark_visitors import json_to_txt, json_to_table


def test_robots_txt_creation():
    robots_json = json.loads(Path("test_files/robots.json").read_text(encoding="utf-8"))
    robots_txt = json_to_txt(robots_json)
    assert Path("test_files/robots.txt").read_text(encoding="utf-8") == robots_txt


def test_table_of_bot_metrices_md():
    robots_json = json.loads(Path("test_files/robots.json").read_text(encoding="utf-8"))
    robots_table = json_to_table(robots_json)
    assert Path("test_files/table-of-bot-metrics.md").read_text(encoding="utf-8") == robots_table
