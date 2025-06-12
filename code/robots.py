#!/usr/bin/env python3
import json
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path

def load_robots_json():
    return json.loads(Path("./robots.json").read_text(encoding="utf-8"))

def get_agent_soup():
    session = requests.Session()
    try:
        response = session.get("https://darkvisitors.com/agents")
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not gather the current agents from https://darkvisitors.com/agents")
        return
    return BeautifulSoup(response.text, "html.parser")

def updated_robots_json(soup):
    existing_content = load_robots_json()
    to_include = ["AI Agents", "AI Assistants", "AI Data Scrapers", "AI Search Crawlers", "Undocumented AI Agents"]
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

            operator = default_value
            if "operated by " in desc:
                try:
                    operator = desc.split("operated by ", 1)[1].split(".", 1)[0].strip()
                except Exception as e:
                    print(f"Error: {e}")

            def consolidate(field: str, value: str) -> str:
                if name not in existing_content:
                    return value
                if field not in existing_content[name]:
                    return value
                if (
                    existing_content[name][field] in default_values
                    and value not in default_values
                ):
                    return value
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
    return {k: existing_content[k] for k in sorted_keys}

def clean_robot_name(name):
    return re.sub(r"\u2011", "-", name)

def ingest_darkvisitors():
    old = load_robots_json()
    soup = get_agent_soup()
    if soup:
        robots_json = updated_robots_json(soup)
        print("robots.json is unchanged." if robots_json == old else "robots.json got updates.")
        Path("./robots.json").write_text(json.dumps(robots_json, indent=4), encoding="utf-8")

def json_to_txt(robots_json):
    agents = [
        ua for name, data in robots_json.items()
        for ua in [name] + data.get("ua-synonyms", [])
    ]
    txt = "\n".join(f"User-agent: {ua}" for ua in agents)
    txt += "\nDisallow: /\n"
    return txt

def escape_md(s):
    return re.sub(r"([]*\\|`(){}<>#+-.!_[])", r"\\\1", s)

def json_to_table(robots_json):
    table = "| Name | Operator | Respects `robots.txt` | Data use | Visit regularity | Description |\n"
    table += "|------|----------|-----------------------|----------|------------------|-------------|\n"
    for name, robot in robots_json.items():
        table += f'| {escape_md(name)} | {robot["operator"]} | {robot["respect"]} | {robot["function"]} | {robot["frequency"]} | {robot["description"]} |\n'
    return table

def list_to_pcre(uas):
    return f"({'|'.join(map(re.escape, uas))})"

def json_to_htaccess(robot_json):
    all_uas = [
        ua for name, data in robot_json.items()
        for ua in [name] + data.get("ua-synonyms", [])
    ]
    return (
        "RewriteEngine On\n"
        f"RewriteCond %{{HTTP_USER_AGENT}} {list_to_pcre(all_uas)} [NC]\n"
        "RewriteRule !^/?robots\\.txt$ - [F,L]\n"
    )

def json_to_nginx(robot_json):
    all_uas = [
        ua for name, data in robot_json.items()
        for ua in [name] + data.get("ua-synonyms", [])
    ]
    return f'if ($http_user_agent ~* "{list_to_pcre(all_uas)}") {{\n    return 403;\n}}'

def json_to_caddy(robot_json):
    all_uas = [
        ua for name, data in robot_json.items()
        for ua in [name] + data.get("ua-synonyms", [])
    ]
    return (
        "@aibots {\n"
        f"        header_regexp User-Agent \"{list_to_pcre(all_uas)}\"\n"
        "}"
    )

def json_to_haproxy(robots_json):
    return "\n".join(
        ua for name, data in robots_json.items()
        for ua in [name] + data.get("ua-synonyms", [])
    )

def update_file_if_changed(file_name, converter):
    new_content = converter(load_robots_json())
    filepath = Path(file_name)
    filepath.touch()
    old_content = filepath.read_text(encoding="utf-8")
    if old_content == new_content:
        print(f"{file_name} is already up to date.")
    else:
        Path(file_name).write_text(new_content, encoding="utf-8")
        print(f"{file_name} has been updated.")

def conversions():
    update_file_if_changed("robots.txt", json_to_txt)
    update_file_if_changed("table-of-bot-metrics.md", json_to_table)
    update_file_if_changed(".htaccess", json_to_htaccess)
    update_file_if_changed("nginx-block-ai-bots.conf", json_to_nginx)
    update_file_if_changed("Caddyfile", json_to_caddy)
    update_file_if_changed("haproxy-block-ai-bots.txt", json_to_haproxy)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update the robots.json file from darkvisitors.com")
    parser.add_argument("--convert", action="store_true", help="Generate output files from robots.json")
    args = parser.parse_args()
    if not (args.update or args.convert):
        print("ERROR: please provide one of the possible flags.")
        parser.print_help()
    if args.update:
        ingest_darkvisitors()
    if args.convert:
        conversions()
