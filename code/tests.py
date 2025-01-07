"""These tests can be run with pytest.
This requires pytest: pip install pytest
cd to the `code` directory and run `pytest`
"""

import json
from pathlib import Path

from robots import json_to_txt, json_to_table, json_to_htaccess


def test_robots_txt_creation():
    robots_json = json.loads(Path("test_files/robots.json").read_text())
    robots_txt = json_to_txt(robots_json)
    assert Path("test_files/robots.txt").read_text() == robots_txt


def test_table_of_bot_metrices_md():
    robots_json = json.loads(Path("test_files/robots.json").read_text())
    robots_table = json_to_table(robots_json)
    assert Path("test_files/table-of-bot-metrics.md").read_text() == robots_table


def test_htaccess_creation():
    robots_json = json.loads(Path("test_files/robots.json").read_text())
    robots_htaccess = json_to_htaccess(robots_json)
    assert Path("test_files/.htaccess").read_text() == robots_htaccess
