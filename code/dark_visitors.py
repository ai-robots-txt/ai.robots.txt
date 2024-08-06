import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup

session = requests.Session()
response = session.get("https://darkvisitors.com/agents")
soup = BeautifulSoup(response.text, "html.parser")

existing_content = json.loads(Path("./robots.json").read_text())
to_include = [
    "AI Assistants",
    "AI Data Scrapers",
    "AI Search Crawlers",
    "Archivers",
    "Developer Helpers",
    "Fetchers",
    "Intelligence Gatherers",
    "Scrapers",
    "Search Engine Crawlers",
    "SEO Crawlers",
    "Uncategorized",
    "Undocumented AI Agents"
]

for section in soup.find_all("div", {"class": "agent-links-section"}):
    category = section.find("h2").get_text()
    for agent in section.find_all("a", href=True):
        name = agent.find("div", {"class": "agent-name"}).get_text().strip()
        desc = agent.find("p").get_text().strip()

        # TODO: there seems to be a typo?
        default_values = {
            "Unclear at this time.", 
            "No information. provided.", 
            "No information.",
            "No explicit frequency provided."
        }
        default_value = "Unclear at this time."
        
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
            if existing_content[name][field] in default_values:
                return value
            # Existing value
            return existing_content[name][field]

        existing_content[name] = {
            "operator": consolidate("operator", operator),
            "respect": consolidate("respect", default_value),
            "function": consolidate("function", f"{category}"),
            "frequency": consolidate("frequency", default_value),
            "description": consolidate("description", f"{desc} More info can be found at https://darkvisitors.com/agents{agent['href']}")
        }

print(f"Total: {len(existing_content)}")
Path("./robots.json").write_text(json.dumps(existing_content, indent=4))