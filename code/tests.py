#!/usr/bin/env python3
"""To run these tests just execute this script."""

import json
import re
import unittest

from robots import (
    consolidate,
    default_value,
    default_values,
    json_to_caddy,
    json_to_haproxy,
    json_to_htaccess,
    json_to_lighttpd,
    json_to_nginx,
    json_to_table,
    json_to_txt,
    list_to_pcre,
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


class TestUserAgentPatternGeneration(unittest.TestCase):
    def test_agents_match_user_agents_by_prefix_or_substring(self):
        pattern = re.compile(
            list_to_pcre({"Spider": {}, "ExampleBot": {}}), re.IGNORECASE
        )

        self.assertIsNotNone(pattern.search("Spider"))
        self.assertIsNotNone(pattern.search("spider"))
        self.assertIsNotNone(pattern.search("Mozilla/5.0 ExampleBot/1.0"))

    def test_generated_regex_against_real_user_agents(self):
        from pathlib import Path
        robots_json_path = Path(__file__).parent.parent / "robots.json"
        if robots_json_path.exists():
            with open(robots_json_path, "rt", encoding="utf-8") as f:
                robots_dict = json.load(f)
        else:
            robots_dict = self.loadJson("test_files/robots.json")

        pattern = re.compile(list_to_pcre(robots_dict), re.IGNORECASE)

        user_agents = [
            "CCBot/2.0 (https://commoncrawl.org/faq/)",
            "Claude-User (claude-code/2.1.220; +https://support.anthropic.com/)",
            "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
            "meta-externalagent/1.1 (+https://developers.facebook.com/docs/sharing/webmasters/crawler)",
            "Scrapy/2.16.0 (+https://scrapy.org)",
        ]

        for ua in user_agents:
            with self.subTest(user_agent=ua):
                self.assertIsNotNone(pattern.search(ua))

    def test_generated_regex_does_not_match_non_ai_user_agents(self):
        from pathlib import Path
        robots_json_path = Path(__file__).parent.parent / "robots.json"
        if robots_json_path.exists():
            with open(robots_json_path, "rt", encoding="utf-8") as f:
                robots_dict = json.load(f)
        else:
            robots_dict = self.loadJson("test_files/robots.json")

        pattern = re.compile(list_to_pcre(robots_dict), re.IGNORECASE)

        non_ai_user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
            "curl/7.68.0",
            "Wget/1.20.3 (linux-gnu)",
        ]

        for ua in non_ai_user_agents:
            with self.subTest(user_agent=ua):
                self.assertIsNone(pattern.search(ua))


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

class TestRobotsNameCleaning(unittest.TestCase):
    def test_clean_name(self):
        from robots import clean_robot_name

        self.assertEqual(clean_robot_name("Perplexity‑User"), "Perplexity-User")

class TestCaddyfileGeneration(unittest.TestCase, RobotsUnittestExtensions):
    maxDiff = 8192

    def setUp(self):
        self.robots_dict = self.loadJson("test_files/robots.json")

    def test_caddyfile_generation(self):
        robots_caddyfile = json_to_caddy(self.robots_dict)
        self.assertEqualsFile("test_files/Caddyfile", robots_caddyfile)

class TestLighttpdConfigGeneration(unittest.TestCase, RobotsUnittestExtensions):
    maxDiff = 8192

    def setUp(self):
        self.robots_dict = self.loadJson("test_files/robots.json")

    def test_lighttpd_generation(self):
        robots_lighttpd = json_to_lighttpd(self.robots_dict)
        self.assertEqualsFile("test_files/lighttpd-block-ai-bots.conf", robots_lighttpd)


class TestConsolidate(unittest.TestCase, RobotsUnittestExtensions):
    maxDiff = 8192

    def test_new_item(self):
        existing = {}
        self.assertEqual("George Jetson", consolidate(existing, "rosie", "operator", "George Jetson"))
        
    def test_ignores_defaults(self):
        existing = {"rosie": { "operator": "George Jetson"}}
        self.assertEqual("George Jetson", consolidate(existing, "rosie", "operator", default_value))
        
    def test_new_description(self):
        existing = {"rosie": { "description": default_value}}
        self.assertEqual("Rosie is the robot maid from The Jetsons, an American animated sitcom", 
                         consolidate(existing, "rosie", "description", "Rosie is the robot maid from The Jetsons, an American animated sitcom"))

if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(__file__))

    unittest.main(verbosity=2)
