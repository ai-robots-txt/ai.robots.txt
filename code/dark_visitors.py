import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def get_updated_robots_json():
    session = requests.Session()
    response = session.get("https://darkvisitors.com/agents")
    soup = BeautifulSoup(response.text, "html.parser")

    existing_content = json.loads(Path("./robots.json").read_text())
    to_include = [
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


def json_to_txt(robots_json):
    robots_txt = "\n".join(f"User-agent: {k}" for k in robots_json.keys())
    robots_txt += "\nDisallow: /\n"
    return robots_txt


def json_to_table(robots_json):
    table = "| Name | Operator | Respects `robots.txt` | Data use | Visit regularity | Description |\n"
    table += "|-----|----------|-----------------------|----------|------------------|-------------|\n"

    for name, robot in robots_json.items():
        table += f'| {name} | {robot["operator"]} | {robot["respect"]} | {robot["function"]} | {robot["frequency"]} | {robot["description"]} |\n'

    return table


if __name__ == "__main__":
    robots_json = get_updated_robots_json()
    Path("./robots.json").write_text(json.dumps(robots_json, indent=4))
    Path("./robots.txt").write_text(json_to_txt(robots_json))
    Path("./table-of-bot-metrics.md").write_text(json_to_table(robots_json))
