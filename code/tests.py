#!/usr/bin/env python3
"""To run these tests just execute this script."""

import json
import unittest
import re

from robots import (
    json_to_txt,
    json_to_table,
    json_to_htaccess,
    json_to_nginx,
    json_to_haproxy,
    json_to_caddy,
    clean_robot_name
)


class RobotsUnittestExtensions:
    def loadJson(self, pathname):
        with open(pathname, "rt") as f:
            return json.load(f)

    def assertEqualsFile(self, f, s):
        with open(f, "rt") as f:
            f_contents = f.read()
        return self.assertMultiLineEqual(f_contents, s)


class TestRobotsTXTGeneration(unittest.TestCase, RobotsUnittestExtensions):
    maxDiff = 8192

    def setUp(self):
        self.robots_dict = self.loadJson("test_files/robots.json")

    def test_robots_txt_generation(self):
        robots_txt = json_to_txt(self.robots_dict)
        self.assertEqualsFile("test_files/robots.txt", robots_txt)


class TestTableMetricsGeneration(unittest.TestCase, RobotsUnittestExtensions):
    maxDiff = 32768

    def setUp(self):
        self.robots_dict = self.loadJson("test_files/robots.json")

    def test_table_generation(self):
        robots_table = json_to_table(self.robots_dict)
        self.assertEqualsFile("test_files/table-of-bot-metrics.md", robots_table)


class TestHtaccessGeneration(unittest.TestCase, RobotsUnittestExtensions):
    maxDiff = 8192

    def setUp(self):
        self.robots_dict = self.loadJson("test_files/robots.json")

    def test_htaccess_generation(self):
        robots_htaccess = json_to_htaccess(self.robots_dict)
        self.assertEqualsFile("test_files/.htaccess", robots_htaccess)


class TestNginxConfigGeneration(unittest.TestCase, RobotsUnittestExtensions):
    maxDiff = 8192

    def setUp(self):
        self.robots_dict = self.loadJson("test_files/robots.json")

    def test_nginx_generation(self):
        robots_nginx = json_to_nginx(self.robots_dict)
        self.assertEqualsFile("test_files/nginx-block-ai-bots.conf", robots_nginx)


class TestHaproxyConfigGeneration(unittest.TestCase, RobotsUnittestExtensions):
    maxDiff = 8192

    def setUp(self):
        self.robots_dict = self.loadJson("test_files/robots.json")

    def test_haproxy_generation(self):
        robots_haproxy = json_to_haproxy(self.robots_dict)
        self.assertEqualsFile("test_files/haproxy-block-ai-bots.txt", robots_haproxy)


class TestCaddyfileGeneration(unittest.TestCase, RobotsUnittestExtensions):
    maxDiff = 8192

    def setUp(self):
        self.robots_dict = self.loadJson("test_files/robots.json")

    def test_caddyfile_generation(self):
        robots_caddyfile = json_to_caddy(self.robots_dict)
        self.assertEqualsFile("test_files/Caddyfile", robots_caddyfile)


class TestRobotsNameCleaning(unittest.TestCase):
    def test_clean_name(self):
        self.assertEqual(clean_robot_name("Perplexity‑User"), "Perplexity-User")


class TestUASynonymSupport(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            "MainBot": {
                "ua-synonyms": ["mainbot/1.0", "Main-Bot"],
                "operator": "TestCorp",
                "respect": "No",
                "function": "Test",
                "frequency": "Often",
                "description": "A test bot"
            }
        }

    def test_robots_txt_includes_synonyms(self):
        output = json_to_txt(self.test_data)
        for variant in ["MainBot", "mainbot/1.0", "Main-Bot"]:
            self.assertIn(f"User-agent: {variant}", output)

    def test_htaccess_includes_synonyms(self):
        output = json_to_htaccess(self.test_data)
        pattern = r"(MainBot|mainbot/1\.0|Main\-Bot)"
        self.assertRegex(output, pattern)


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(__file__))
    unittest.main(verbosity=2)

