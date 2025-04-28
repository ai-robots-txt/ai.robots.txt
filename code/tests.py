#!/usr/bin/env python3
"""To run these tests just execute this script."""

import json
import unittest

from robots import json_to_txt, json_to_table, json_to_htaccess, json_to_nginx, json_to_haproxy

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

class TestRobotsNameCleaning(unittest.TestCase):
    def test_clean_name(self):
        from robots import clean_robot_name

        self.assertEqual(clean_robot_name("Perplexity‑User"), "Perplexity-User")

if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(__file__))

    unittest.main(verbosity=2)
