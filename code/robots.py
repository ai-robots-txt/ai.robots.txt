#!/usr/bin/env python3

import json
import re
import requests

from bs4 import BeautifulSoup
from pathlib import Path


def load_robots_json():
    """Load the robots.json contents into a dictionary."""
    return json.loads(Path("./robots.json").read_text(encoding="utf-8"))


def get_agent_soup():
    """Retrieve current known agents from darkvisitors.com"""
    session = requests.Session()
    try:
        response = session.get("https://darkvisitors.com/agents")
    except requests.exceptions.ConnectionError:
        print(
            "ERROR: Could not gather the current agents from https://darkvisitors.com/agents"
        )
        return
    return BeautifulSoup(response.text, "html.parser")


def updated_robots_json(soup):
    """Update AI scraper information with data from darkvisitors."""
    existing_content = load_robots_json()
    to_include = [
        "AI Agents",
        "AI Assistants",
        "AI Data Scrapers",
        "AI Search Crawlers",
        # "Archivers",
        # "Developer Helpers",
        # "Fetchers",
        # "Intelligence Gatherers",
        # "Scrapers",
        # "Search Engine Crawlers",
        # "SEO Crawlers",
        # "Uncategorized",
        "Undocumented AI Agents",
    ]

    for section in soup.find_all("div", {"class": "agent-links-section"}):
        category = section.find("h2").get_text()
        if category not in to_include:
            continue
        for agent in section.find_all("a", href=True):
            name = agent.find("div", {"class": "agent-name"}).get_text().strip()
            name = clean_robot_name(name)
            desc = agent.find("p").get_text().strip()

            default_values = {
                "Unclear at this time.",
                "No information provided.",
                "No information.",
                "No explicit frequency provided.",
            }
            default_value = "Unclear at this time."

            # Parse the operator information from the description if possible
            operator = default_value
            if "operated by " in desc:
                try:
                    operator = desc.split("operated by ", 1)[1].split(".", 1)[0].strip()
                except Exception as e:
                    print(f"Error: {e}")

            def consolidate(field: str, value: str) -> str:
                # New entry
                if name not in existing_content:
                    return value
                # New field
                if field not in existing_content[name]:
                    return value
                # Unclear value
                if (
                    existing_content[name][field] in default_values
                    and value not in default_values
                ):
                    return value
                # Existing value
                return existing_content[name][field]

            existing_content[name] = {
                "operator": consolidate("operator", operator),
                "respect": consolidate("respect", default_value),
                "function": consolidate("function", f"{category}"),
                "frequency": consolidate("frequency", default_value),
                "description": consolidate(
                    "description",
                    f"{desc} More info can be found at https://darkvisitors.com/agents{agent['href']}",
                ),
            }

    print(f"Total: {len(existing_content)}")
    sorted_keys = sorted(existing_content, key=lambda k: k.lower())
    sorted_robots = {k: existing_content[k] for k in sorted_keys}
    return sorted_robots


def clean_robot_name(name):
    """ Clean the robot name by removing some characters that were mangled by html software once. """
    # This was specifically spotted in "Perplexity-User"
    # Looks like a non-breaking hyphen introduced by the HTML rendering software
    # Reading the source page for Perplexity: https://docs.perplexity.ai/guides/bots
    # You can see the bot is listed several times as "Perplexity-User" with a normal hyphen, 
    # and it's only the Row-Heading that has the special hyphen
    # 
    # Technically, there's no reason there wouldn't someday be a bot that 
    # actually uses a non-breaking hyphen, but that seems unlikely,
    # so this solution should be fine for now.
    result = re.sub(r"\u2011", "-", name)
    if result != name:
        print(f"\tCleaned '{name}' to '{result}' - unicode/html mangled chars normalized.")
    return result


def ingest_darkvisitors():
    old_robots_json = load_robots_json()
    soup = get_agent_soup()
    if soup:
        robots_json = updated_robots_json(soup)
        print(
            "robots.json is unchanged."
            if robots_json == old_robots_json
            else "robots.json got updates."
        )
        Path("./robots.json").write_text(
            json.dumps(robots_json, indent=4), encoding="utf-8"
        )


def json_to_txt(robots_json):
    """Compose the robots.txt from the robots.json file."""
    robots_txt = "\n".join(f"User-agent: {k}" for k in robots_json.keys())
    robots_txt += "\nDisallow: /\n"
    return robots_txt


def escape_md(s):
    return re.sub(r"([]*\\|`(){}<>#+-.!_[])", r"\\\1", s)


def json_to_table(robots_json):
    """Compose a markdown table with the information in robots.json"""
    table = "| Name | Operator | Respects `robots.txt` | Data use | Visit regularity | Description |\n"
    table += "|------|----------|-----------------------|----------|------------------|-------------|\n"

    for name, robot in robots_json.items():
        table += f'| {escape_md(name)} | {robot["operator"]} | {robot["respect"]} | {robot["function"]} | {robot["frequency"]} | {robot["description"]} |\n'

    return table


def list_to_pcre(lst):
    # Python re is not 100% identical to PCRE which is used by Apache, but it
    # should probably be close enough in the real world for re.escape to work.
    formatted = "|".join(map(re.escape, lst))
    return f"({formatted})"


def json_to_htaccess(robot_json):
    # Creates a .htaccess filter file. It uses a regular expression to filter out
    # User agents that contain any of the blocked values.
    htaccess = "RewriteEngine On\n"
    htaccess += f"RewriteCond %{{HTTP_USER_AGENT}} {list_to_pcre(robot_json.keys())} [NC]\n"
    htaccess += "RewriteRule !^/?robots\\.txt$ - [F,L]\n"
    return htaccess

def json_to_nginx(robot_json):
    # Creates an Nginx config file. This config snippet can be included in 
    # nginx server{} blocks to block AI bots.
    config = f"if ($http_user_agent ~* \"{list_to_pcre(robot_json.keys())}\") {{\n    return 403;\n}}"
    return config


def json_to_caddy(robot_json):
    caddyfile = "@aibots {\n    "
    caddyfile += f'    header_regexp User-Agent "{list_to_pcre(robot_json.keys())}"'
    caddyfile += "\n}"
    return caddyfile

def json_to_haproxy(robots_json):
    # Creates a source file for HAProxy. Follow instructions in the README to implement it.
    txt = "\n".join(f"{k}" for k in robots_json.keys())
    return txt



def update_file_if_changed(file_name, converter):
    """Update files if newer content is available and log the (in)actions."""
    new_content = converter(load_robots_json())
    filepath = Path(file_name)
    # "touch" will create the file if it doesn't exist yet
    filepath.touch()
    old_content = filepath.read_text(encoding="utf-8")
    if old_content == new_content:
        print(f"{file_name} is already up to date.")
    else:
        Path(file_name).write_text(new_content, encoding="utf-8")
        print(f"{file_name} has been updated.")


def conversions():
    """Triggers the conversions from the json file."""
    update_file_if_changed(file_name="./robots.txt", converter=json_to_txt)
    update_file_if_changed(
        file_name="./table-of-bot-metrics.md",
        converter=json_to_table,
    )
    update_file_if_changed(
        file_name="./.htaccess",
        converter=json_to_htaccess,
    )
    update_file_if_changed(
        file_name="./nginx-block-ai-bots.conf",
        converter=json_to_nginx,
    )
    update_file_if_changed(
        file_name="./Caddyfile",
        converter=json_to_caddy
      
    update_file_if_changed(
        file_name="./haproxy-block-ai-bots.txt",
        converter=json_to_haproxy,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
        prog="ai-robots",
        description="Collects and updates information about web scrapers of AI companies.",
        epilog="One of the flags must be set.\n",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update the robots.json file with data from darkvisitors.com/agents",
    )
    parser.add_argument(
        "--convert",
        action="store_true",
        help="Create the robots.txt and markdown table from robots.json",
    )
    args = parser.parse_args()

    if not (args.update or args.convert):
        print("ERROR: please provide one of the possible flags.")
        parser.print_help()

    if args.update:
        ingest_darkvisitors()
    if args.convert:
        conversions()
